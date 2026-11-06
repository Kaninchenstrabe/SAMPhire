def main(data):
    temp=sorted(data)
    for i in range(len(data)):
        data[i]=temp[i].item()
    return data