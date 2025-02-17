import re
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI # type: ignore

tree_files = ['trees/tree1.txt', 'trees/tree2.txt', 'trees/tree3.txt', 'trees/tree4.txt', 'trees/tree5.txt']
actionfile = './action.txt'
controller = SimpleSwitchThriftAPI(9090)
#controller = 1

# read the action.text, find the actions for different classes.
def find_action(textfile):
    action = []
    f = open(textfile)
    for line in f:
        n = re.findall(r"class", line)
        if n:
            fea = re.findall(r"\d", line)
            action.append(int(fea[1]))
    f.close()
    return action

# read the tree model, search the threshold value
def find_feature(textfile):
    f = open(textfile)
    line = f.readline()
    fs = re.findall('\d+', line)
    line = f.readline()
    ps = re.findall('\d+', line)
    line = f.readline()
    ipi = re.findall('\d+', line)
    line = f.readline()
    ifi = re.findall('\d+', line)
    f.close()
    fs = [int(i) for i in fs]
    ps = [int(i) for i in ps]
    ipi = [int(i) for i in ipi]
    ifi = [int(i) for i in ifi]
    return fs, ps, ipi, ifi

# read the leaf node description and find the corresponding ranges
def find_classification(textfile, fs, ps, ipi, ifi):
    fea = []
    sign = []
    num = []
    f = open(textfile, 'r')
    for line in f:
        n = re.findall(r"when", line)
        if n:
            fea.append(re.findall(r"(fs|ps|ipi|ifi)", line))
            sign.append(re.findall(r"(<=|>)", line))
            num.append(re.findall(r"\d+\.?\d*", line))
    f.close()

    fs_values = []
    ps_values = []
    ipi_values = []
    ifi_values = []
    classification = []

    for i in range(len(fea)):
        feature1 = [i for i in range(len(fs) + 1)]
        feature2 = [i for i in range(len(ps) + 1)]
        feature3 = [i for i in range(len(ipi) + 1)]
        feature4 = [i for i in range(len(ifi) + 1)]
        for j, feature in enumerate(fea[i]):
            if feature == 'fs':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = fs.index(thres)
                if sig == '<=':
                    while id < len(fs):
                        if id + 1 in feature1:
                            feature1.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature1:
                            feature1.remove(id)
                        id = id - 1
            elif feature == 'ps':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = ps.index(thres)
                if sig == '<=':
                    while id < len(ps):
                        if id + 1 in feature2:
                            feature2.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature2:
                            feature2.remove(id)
                        id = id - 1
            elif feature == 'ipi':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = ipi.index(thres)
                if sig == '<=':
                    while id < len(ipi):
                        if id + 1 in feature3:
                            feature3.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature3:
                            feature3.remove(id)
                        id = id - 1
            elif feature == 'ifi':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = ifi.index(thres)
                if sig == '<=':
                    while id < len(ifi):
                        if id + 1 in feature4:
                            feature4.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature4:
                            feature4.remove(id)
                        id = id - 1
        fs_values.append(feature1)
        ps_values.append(feature2)
        ipi_values.append(feature3)
        ifi_values.append(feature4)
        a = len(num[i])
        classification.append(num[i][a - 1])
    return (fs_values, ps_values, ipi_values, ifi_values, classification)

def find_features_forest(tree_files):
    all_fs = []
    all_ps = []
    all_ipi = []
    all_ifi = []
    for file in tree_files:
        fs, ps, ipi, ifi = find_feature(file)
        #all_features.append((fs, ps, ipi, ifi))
        all_fs.append(fs)
        all_ps.append(ps)
        all_ipi.append(ipi)
        all_ifi.append(ifi)
    return all_fs, all_ps, all_ipi, all_ifi

def find_classifications_forest(tree_files, all_fs, all_ps, all_ipi, all_ifi):
    all_fs_values = []
    all_ps_values = []
    all_ipi_values = []
    all_ifi_values = []
    all_classification = []
    for i, file in enumerate(tree_files):
        #fs, ps, ipi, ifi = all_features[i]
        fs_values, ps_values, ipi_values, ifi_values, classification = find_classification(file, all_fs[i], all_ps[i], all_ipi[i], all_ifi[i])
        all_fs_values.append(fs_values)
        all_ps_values.append(ps_values)
        all_ipi_values.append(ipi_values)
        all_ifi_values.append(ifi_values)
        all_classification.append(classification)
        #all_classifications.append(classifications)

    return all_fs_values, all_ps_values, all_ipi_values, all_ifi_values, all_classification
'''
def vote_on_classification(all_classifications):
    final_classification = []
    
    # Itera por todas as classificações para cada entrada (cada "coluna" em all_classifications)
    for classifications in all_classifications:
        # Conta as ocorrências de cada classe
        counts = {}
        for classification in classifications:
            counts[classification] = counts.get(classification, 0) + 1
        
        # Encontra a classe com mais votos
        voted_class = max(counts, key=counts.get)
        
        # Adiciona a classe com mais votos à lista final de classificações
        final_classification.append(voted_class)
    
    return final_classification
'''

def writeactionrule(controller, a, b, c, d, action, tree, result):
    print([a, b, c, d])
    controller.table_add(f"t{tree}_classify_exact", f"t{tree}_{action}", [f"{a[0]}->{a[1]}", f"{b[0]}->{b[1]}", f"{c[0]}->{c[1]}", f"{d[0]}->{d[1]}"], [str(result)] ,  prio=0)
    print("add action rule")

def writefeatureXrule(controller, range, ind, tree, table, action):
    print(range)
    print(ind)
    controller.table_add(f"t{tree}_{table}", action, [f"{range[0]}->{range[1]}"], [str(ind)])
    print(f"add {table} rule")


def main():

    all_fs, all_ps, all_ipi, all_ifi = find_features_forest(tree_files) #fs, ps, ipi, ifi = find_feature(inputfile)
    print("all features: \n", all_fs) #print(f"fs = {fs},\n ps = {ps},\n ipi = {ipi},\n ifi = {ifi}\n")
    
    all_fs_values, all_ps_values, all_ipi_values, all_ifi_values, all_classification = find_classifications_forest(tree_files, all_fs, all_ps, all_ipi, all_ifi) #fs_values, ps_values, ipi_values, ifi_values, classification = find_classification(inputfile, fs, ps, ipi, ifi)
    #print("all_classification: \n", all_classifications)#print(f"fs_values = {fs_values},\n ps_values = {ps_values},\n ipi_values = {ipi_values},\n ifi_values = {ifi_values},\n classification = {classification}\n")
    print("all classification: \n",  all_fs_values,"\n", all_classification)

    #final_classification = vote_on_classification(all_classifications)
    #print("final_classification: \n", final_classification)

    action = find_action(actionfile)
    print(f"action = {action}\n")

    

    # parameter for random forest
    for j in range(len(all_classification)):
        for i in range(len(all_classification[j])):
            a = all_fs_values[j][i]
            #print(type(a), a)
            id = len(a) - 1
            del a[1:id]
            if len(a) == 1:
                a.append(a[0])
            b = all_ps_values[j][i]
            id = len(b) - 1
            del b[1:id]
            if len(b) == 1:
                b.append(b[0])
            c = all_ipi_values[j][i]
            id = len(c) - 1
            del c[1:id]
            if len(c) == 1:
                c.append(c[0])
            d = all_ifi_values[j][i]
            id = len(d) - 1
            del d[1:id]
            if len(d) == 1:
                d.append(d[0])

            ind = int(all_classification[j][i])
            ac = action[ind]
            a = [i + 1 for i in a]
            b = [i + 1 for i in b]
            c = [i + 1 for i in c]
            d = [i + 1 for i in d]

            if ac == 0:
                pass
            else:
                writeactionrule(controller, a, b, c, d, 'set_result', j+1, ind)

    # for feature1 table
    for j in range(len(all_fs)):
        all_fs[j].append(0)
        all_fs[j].append(100000)
        all_fs[j].sort()
        for i in range(len(all_fs[j]) - 1):
            writefeatureXrule(controller, all_fs[j][i:i + 2], i + 1, j+1, "feature1_exact", "set_actionselect1")

    # for feature2 table
    for j in range(len(all_ps)):
        all_ps[j].append(0)
        all_ps[j].append(100000)
        all_ps[j].sort()
        for i in range(len(all_ps[j]) - 1):
            writefeatureXrule(controller, all_ps[j][i:i + 2], i + 1, j+1, "feature2_exact", "set_actionselect2")

    # for feature3 table
    for j in range(len(all_ipi)):
        all_ipi[j].append(0)
        all_ipi[j].append(1000000)
        all_ipi[j].sort()
        for i in range(len(all_ipi[j]) - 1):
            writefeatureXrule(controller, all_ipi[j][i:i + 2], i + 1, j+1, "feature3_exact", "set_actionselect3")

    # for feature4 table (ifi)
    for j in range(len(all_ifi)):
        all_ifi[j].append(0)
        all_ifi[j].append(1000000)
        all_ifi[j].sort()
        for i in range(len(all_ifi[j]) - 1):
            writefeatureXrule(controller, all_ifi[j][i:i + 2], i + 1, j+1, "feature4_exact", "set_actionselect4")

    

if __name__ == "__main__":
    main()