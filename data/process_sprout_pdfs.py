from data_point import TempEditOutcome, EditOutcome, DataPoint
import PyPDF2 as pypdf
import pickle
import os


PDF_DIR = '../data/SPROUT/pdfs'
COUNT_DIR = '../data/SPROUT/counts'
DATA_POINTS_DIR = '../data/data_points'
OTHER_LEN = len('Other')


paths = (
    (x.replace('.pdf', ''), os.path.join(PDF_DIR, x), os.path.join(COUNT_DIR, f"counts-{x.split('.')[0]}.txt"))
    for x in os.listdir(PDF_DIR)
    if x.endswith('.pdf')
)


def sliding_window(l, n):
    for a in range(0, len(l)-n+1):
        yield a, l[a:a+n]


for i, (general_name, pdf_path, count_path) in enumerate(paths):
    print(f"{i}: {pdf_path.split('/')[-1]}")

    breakout = False

    with open(pdf_path, 'rb') as pdf_file:
        try:
            reader = pypdf.PdfFileReader(pdf_file)
            text = ''.join(reader.getPage(0).extractText().split())
        except OSError:
            breakout = True

    if breakout:
        print('Cancelled!')
        continue

    # Commonly found 'llOther' or 'lOther' pattern in the pdfs.
    l_index = next(i for i, x in enumerate(text) if x not in 'ACGTURYKMSWBDHVN-')

    if text[l_index-1] == '-':  # Accounting for negative sign in subsequent indels
        l_index -= 1

    other_index = next(l_index + i for i, x in enumerate(text[l_index:]) if x != 'l')

    if text[other_index:other_index+OTHER_LEN] == 'Other':
        other_index += OTHER_LEN

    no_variant_index = text.find('novariant') or text.find('Reference')

    sequences_raw = text[:l_index]
    raw_events = text[other_index:no_variant_index]   # Removes all whitespace

    event_strs = ['no variant'] if 'novariant' in text else []
    region = ''
    comma_on = 0
    addons = 0

    for j, c in enumerate(raw_events):
        region += c

        if c == 'I' or c == 'D':
            event_strs.append(region)
            region = ''

            if comma_on > 0:
                event_strs = event_strs[:-(comma_on+1)]
                addons += 1
                comma_on = -2
            elif comma_on == -1:
                event_strs = event_strs[:-1]
                comma_on = -2
            else:
                comma_on = 0
        elif c == ',':
            comma_on += 1
        elif 'S' in region:  # SNV - all future regions will be SNV
            event_strs.extend('SNV:' + x for x in raw_events[j:].split('SNV:')[1:])
            break

    if len(event_strs) == 0:
        print('Cancelled!')
        continue

    num_bases_per_column = len(event_strs) + addons + 1  # Accounting for reference

    assert len(sequences_raw) % num_bases_per_column == 0

    sequences = (
        sequences_raw[i:(i+num_bases_per_column)]
        for i in range(0, len(sequences_raw)-num_bases_per_column+1, num_bases_per_column)
    )

    reference = ''.join(x[-1] for x in sequences)

    assert len(reference) == 60

    half_point = len(reference) // 2
    pam_start = half_point + 3  # Always 3bp after the half point
    pam_site = reference[pam_start:pam_start+3]
    guide_sequence = reference[pam_start-20:pam_start]

    assert pam_site[1:] == 'GG'  # Cas9 PAM is 'NGG'

    with open(count_path, 'r') as counts_file:
        samples, *names_and_counts, other, null = [eval(f'[{x}]') for x in counts_file.read().split('\n')]

    sample_totals = other[1:]
    sample_events = [[] for _ in range(len(samples))]

    for name, *counts in names_and_counts:
        if name in event_strs:
            if name == 'no variant':
                start_point = 0
                indel = 0
            elif 'SNV' in name:
                start_point = name.split(':')[1]
                indel = 0
            else:
                event_type = name[-1]
                str_start, str_size = name[:-1].split(':')
                start_point = int(str_start)
                indel = (-1 if event_type == 'D' else 1) * int(str_size)

            for j, count in enumerate(counts):
                sample_events[j].append(TempEditOutcome(start_point, indel, count))

        sample_totals = [x + y for x, y in zip(sample_totals, counts)]

    for sample_name, event, total in zip(samples, sample_events, sample_totals):
        point = DataPoint(
            sample_name, general_name, guide_sequence, pam_site, cut_site=half_point,
            neighborhood=reference, total_reads=total, events=event
        )

        with open(os.path.join(DATA_POINTS_DIR, f'{sample_name}.pickle'), 'wb') as f:
            pickle.dump(point, f)
