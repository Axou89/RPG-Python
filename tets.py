def Reading(lecture):
    test = "TXTS/" + lecture + ".txt"
    print(test)
    f = open(test,'r')
    message = f.read()
    print(message)
    f.close()

Reading("Guillaume")