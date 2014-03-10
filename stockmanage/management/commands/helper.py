def parse_location(location_code):
        #1.2.3-->1,1.2,1.3
        seperated= location_code.split('.')
        locations=[]
        base=''
        for s in seperated:
            base+=s+'.'
            locations.append(base.rstrip('.'))
        print(locations)
if __name__=="__main__":
    parse_location('1.2.3')