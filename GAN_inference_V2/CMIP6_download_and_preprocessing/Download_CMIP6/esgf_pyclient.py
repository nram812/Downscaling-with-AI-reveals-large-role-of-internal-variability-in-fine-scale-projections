from pyesgf.search import SearchConnection
conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)

ctx = conn.new_context(
    project='CMIP6',
    source_id='ACCESS-CM2',
    experiment_id='historical',
    variable='ua',
    frequency='day',
    variant_label='r4i1p1f1')

ctx.hit_count
result = ctx.search()[0]
files = result.file_context().search()
for file in files:
    print(file.opendap_url)
result.dataset_id
