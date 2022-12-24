# The purpose of this file atm is running extract_xml only once it's
# fully imported, to avoid weird import behavior

import extract_xml

if __name__ == "__main__":
    profile = True
    if profile:
        import cProfile

        cProfile.run("extract_xml.main()", "cprof_assets421.txt")
    else:
        extract_xml.main()
