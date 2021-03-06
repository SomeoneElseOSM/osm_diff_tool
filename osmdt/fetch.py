def fetch(sequence, time='hour'):
    """
    Fetch an OpenStreetMap diff file.

    Parameters
    ----------
    sequence : string or integer
        Diff file sequence desired. Maximum of 9 characters allowed. The value
        should follow the two directory and file name structure from the site,
        e.g. http://planet.osm.org/replication/hour/NNN/NNN/NNN.osc.gz (with
        leading zeros optional).

    time : {'minute', 'hour', or 'day'}, optional
        Denotes the diff file time granulation to be downloaded. The value
        must be a valid directory at http://planet.osm.org/replication/.

    Returns
    -------
    data_stream : class
        A file-like class containing a decompressed data stream from the
        fetched diff file in string format.

    """
    import StringIO
    import gzip
    import requests

    if time not in ['minute','hour','day']:
        raise ValueError('The supplied type of replication file does not exist.')

    sqn = str(sequence).zfill(9)
    url = "http://planet.osm.org/replication/%s/%s/%s/%s.osc.gz" %\
          (time, sqn[0:3], sqn[3:6], sqn[6:9])
    content = requests.get(url)

    if content.status_code == 404:
        raise EnvironmentError('Diff file cannot be found.')
    
    content = StringIO.StringIO(content.content)
    data_stream = gzip.GzipFile(fileobj=content)

    return data_stream
