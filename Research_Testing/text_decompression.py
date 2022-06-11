

class Text_Decompressor(object):
    def decompress(self, compressed_data):
        data = compressed_data.replace(" \n ", "\n").split(" ")
        for i in range(len(data)):
            if self.is_reference(data[i]):
                self.update_data(data, i)

        self.decompressed_data = " ".join(list(data)).replace("~<", "<")

    def update_data(self, data, i):
        ref_distance = self.get_reference_distance(data[i])
        if ref_distance <= i:
            if "\n" == data[i][-1]:
                data[i] = data[i-ref_distance] + "\n"
            elif "\n" == data[i][0]:
                data[i] = "\n" + data[i-ref_distance]
            else:
                data[i] = data[i-ref_distance]

    def is_reference(self, item):
        return "<" in item and "~" not in item

    def get_reference_distance(self, reference):
        return int(reference.split("<")[-1])

    def get_decompressed_data(self):
        return self.decompressed_data