from build_final_pdfs import build, ROOT
if __name__ == '__main__':
    build(ROOT/'validation.md', ROOT/'validation.pdf')
    print('Rebuilt current complete validation.md; no historical PDF used.')
