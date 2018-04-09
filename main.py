import csv
import functools;

class TextSearch():
    ''' ### Text Search
        ### 文字搜索
    '''
    def __init__(self, sourceFile):
        ''' ### Data Read-in
        sourceFile:   [str] Location of the data. Data should be in CSV Format.

        ### 資料讀入
        sourceFile:   [str] 資料來源位址，資料需要是 CSV 格式。
        '''
        self._idx = {};
        self._data = {};
        with open(sourceFile, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f);
            for row in reader:
                idx = int(row[0]);
                self._data[idx] = row[1];
                for c in row[1]:
                    if (c in self._idx):
                        self._idx[c].add(idx);
                    else:
                        self._idx[c] = {idx};
    @staticmethod
    def allIntersect(s):
        return s[0] & TextSearch.allIntersect(s[1:]) if len(s) > 1 else s[0];
    
    @staticmethod
    def allUnion(s):
        return s[0] | TextSearch.allUnion(s[1:]) if len(s) > 1 else s[0];
    
    @staticmethod
    def allDiff(fromSet,sets):
        return fromSet - TextSearch.allUnion(sets);

    @staticmethod
    def sortAsc(a,b):
        return 1 if a>b else -1;

    def query(self, qStr):
        if (" and " in qStr):
            queries = qStr.split(" and ");
            return [idx for idx in sorted(self.allIntersect([{idx for idx in self._idx[q[0]] if q in self._data[idx]} if q[0] in self._idx else set() for q in queries]), key=functools.cmp_to_key(self.sortAsc))];
        elif (" or " in qStr):
            queries = qStr.split(" or ");
            return [idx for idx in sorted(self.allUnion([{idx for idx in self._idx[q[0]] if q in self._data[idx]} if q[0] in self._idx else set() for q in queries]), key=functools.cmp_to_key(self.sortAsc))];
        else:
            queries = qStr.split(" not ");
            has = queries[0];
            notEle = queries[1:];
            return [idx for idx in sorted(self.allDiff({idx for idx in self._idx[has[0]] if has in self._data[idx]}, [{idx for idx in self._idx[q[0]] if q in self._data[idx]} if q[0] in self._idx else set() for q in notEle]), key=functools.cmp_to_key(self.sortAsc))] if has[0] in self._idx else [];


if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query2.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()
    
    # Please implement your algorithm below
    
    # TODO load source data, build search engine

    textData = TextSearch(args.source);

    # TODO compute query result
    allLines = [];
    with open(args.query, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f);
        for row in reader:
            allLines.append(textData.query(row[0]) or ["0"]);

    # TODO output result
    with open(args.output, 'w', newline='') as f:
        f.write("\n".join([",".join([str(c) for c in r]) for r in allLines]));

