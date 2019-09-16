import mmap


class ReadLmpLog:

    def __init__(self, input_name):

        self.f = open(input_name, 'r+b')
        self.fm = mmap.mmap(self.f.fileno(), 0)
        self.f.close()

    def acq_elastic(self, direction):

        key_word = 'C' + str(direction) + 'all'
        mloc = self.fm.find(str.encode(key_word), 0)
        return mloc

    def elastic_arr(self):

        dir_dic = {}
        dir_arr = [11, 22, 33, 44, 55, 66, 12, 13, 23]

        for ele in dir_arr:

            self.fm.seek(self.acq_elastic(ele))
            value = self.fm.readline().decode('utf-8').split()[2]
            keyword = 'C' + str(ele)
            dir_dic[keyword] = float(value)

        return dir_dic

    def bulkmod(self, e):

        bulk_mod = (e.get('C11') + e.get('C22') + e.get('C33') + 2 * (e.get('C12') + e.get('C13') + e.get('C23'))) / 9

        return bulk_mod

    def shearmod(self, e):

        a = e.get('C11') + e.get('C22') + e.get('C33')
        b = e.get('C12') + e.get('C13') + e.get('C23')
        c = e.get('C44') + e.get('C55') + e.get('C66')

        shear_mod = (a - b + 3 * c) / 15
        return shear_mod

    def young_mod(self):
        b = self.bulkmod(self.elastic_arr())
        g = self.shearmod(self.elastic_arr())
        y = 1 / (1 / (3 * g) + 1 / (9 * b))

        return y


if __name__ == '__main__':

    for i in range(9):
        log_obj = ReadLmpLog('lmplog' + str(i + 1))
        young = log_obj.young_mod()
        print(young)