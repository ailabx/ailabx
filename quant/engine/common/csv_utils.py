import requests
def download_csv(url, url_params=None, content_type="text/csv"):
    response = requests.get(url, params=url_params)

    response.raise_for_status()
    response_content_type = response.headers['content-type']
    if response_content_type != content_type:
        raise Exception("Invalid content-type: %s" % response_content_type)

    ret = response.text

    # Remove the BOM
    while not ret[0].isalnum():
        ret = ret[1:]

    return ret