

def paging_filter_sort(query, params):
    paging = params.get('paging')
    if paging:
        limit = paging[0]
        offset = paging[1]
        content_stm = query.offset(offset).limit(limit)
    return content_stm
