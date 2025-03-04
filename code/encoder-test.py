import Encoder

enc = Encoder.Encoder(27, 22)

while True:
    try:
        print(enc.read())
    except:
        pass