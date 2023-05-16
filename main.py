try:
    import lexical_analysis as lx
    code = open('source.txt')
    parsing = lx.parser(code.read())
    code.close()
except:
    print("Unexpected sytax")