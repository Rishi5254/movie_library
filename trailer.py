ma = 'For Peter Parker, life is busy. Between taking out the bad guys as Spider-Man and spending time with the person he loves, Gwen Stacy, high school graduation cannot come quickly enough. Peter has not forgotten about the promise he made to Gwen’s father to protect her by staying away, but that is a promise he cannot keep. Things will change for Peter when a new villain, Electro, emerges, an old friend, Harry Osborn, returns, and Peter uncovers new clues about his past.'

i = 500
print(ma)
print(len(ma))
if len(ma) < 500:
    length = len(ma)
    for _ in range(i-length):
        ma += " "
    print(ma)
    print(len(ma))