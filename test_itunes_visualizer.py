import itunes_visualizer as iv


def test_get_zipcode_info():
    assert "Louisville".upper() == iv.get_zipcode_info("80027")["city"]
    assert "Louisville".upper() == iv.get_zipcode_info("80027-8606")["city"]
    assert "CO".upper() == iv.get_zipcode_info("80027")["state"]

    def test_load_itunes_report(tmpdir):
        content_to_write = """
    Artist Name	Album Name	Track Name	Download Date	Quantity	Country	State	City	Postal Code
    Chance's End		Diamond In Disguise	1/2/2012 12:00:00 AM	1	US	CO	Louisville	80027-8606
    Chance's End		North of Nowhere	1/3/2012 12:00:00 AM	1	US	IL	La grange	60525-7401
    """
        p = tmpdir.join("temp.txt")
        p.write(content_to_write)

        data = iv.load_itunes_report(p)
        print data.dtypes
        assert data["Artist Name"][0] == "Chance's End"
        assert pd.isnull(data["Album Name"][0])
        assert data["Track Name"][0] == "Diamond In Disguise"
        assert data["Track Name"][1] == "North of Nowhere"
        assert data["Download Date"][0] == pd.Timestamp('20120102')
        assert data["Download Date"][1] == pd.Timestamp('20120103')


def test_parse_folder(tmpdir):
    files = [
        "hello.txt",
        "iTunesTrendingReport-01.02.2012-01.08.2012.txt",
        "iTunesTrendingReport-04.27.2015-05.03.2015.txt",
    ]

    dir = tmpdir.mkdir("sub")
    for file in files:
        p = dir.join(file)
        p.write("content")

    out_files = iv.parse_folder_for_itunes_reports(str(tmpdir))
    assert len(out_files) == 2