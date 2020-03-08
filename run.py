import json
import random
import numpy
from gensim.models.fasttext import load_facebook_model
#from nltk.stem import WordNetLemmatizer
#from keras.utils import to_categorical
from nltk.tokenize import TweetTokenizer
from nltk import tokenize

from fuzzywuzzy import fuzz

#lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()
trained_model = None
fasttext_model = None

def load_fasttext():
    global fasttext_model
    fasttext_model = load_facebook_model('wiki-news-300d-1M-subword.bin')


def fasttext_Vec(body):
    tokens = tokenizer.tokenize(body)
    output = numpy.zeros(300)
    for token in tokens:
        try:
            output = numpy.add(output, fasttext_model[token])
        except Exception:
            output = numpy.add(output, numpy.zeros(300))
    return output

def process():
    patients = []
    import csv

    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            #print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
            patient = []
            # process the input

            # patientID
            patient.append(row['GroupID'])

            patient.append(row['PatientID'])

            patient.append(row['Patient Acct #'])

            patient.append(row['First Name'] + ' ' + row['MI'] + ' ' + row['Last Name'])

            patient.append(row['Date of Birth'])

            patient.append(row['Sex'])

            patient.append(row['Current Street 1'])
            patient.append(row['Current Street 2'])
            patient.append(row['Current City'])
            patient.append(row['Current State'])
            patient.append(row['Current Zip Code'])
            
            patient.append(row['Previous First Name'] + ' ' + row['Previous MI'] + ' ' + row['Previous Last Name'])

            patient.append(row['Previous Street 1'])
            patient.append(row['Previous Street 2'])
            patient.append(row['Previous City'])
            patient.append(row['Previous State'])
            patient.append(row['Previous Zip Code'])
            patients.append(patient)

            line_count += 1
        print(f'Processed {line_count} lines.')
    return patients

def check_accuracy(patients, threshold, labels):    
    p_label = int(patients[0][0])
    correct_labels = [[p_label]]
    l_ind = 0
    for i in range(1, len(patients)):
        current_label = int(patients[i][0])
        if current_label != p_label:
            l_ind += 1
            correct_labels.append([])

        correct_labels[l_ind].append(current_label)
        p_label = current_label
    
    #print(correct_labels)

    ind = 0
    correct = 0
    incorrect_ind = []
    accepted_labels = []
    for label_group in correct_labels:
        label_group_nums = []
        label_group_count = []
        for i, _ in enumerate(label_group):
            if labels[ind] not in label_group_nums:
                label_group_nums.append(labels[ind])
                label_group_count.append(1)
            else:
                lb_ind = label_group_nums.index(labels[ind])
                label_group_count[lb_ind] += 1
                
            ind += 1
        
        while(label_group_nums != []):
            max_sim = max(label_group_count)
            lb_ind = label_group_count.index(max_sim)
            guess = label_group_nums[lb_ind]
            
            if guess not in accepted_labels:
                accepted_labels.append(guess)
                correct += max_sim
                break
            
            label_group_count.pop(lb_ind)
            label_group_nums.pop(lb_ind)
            
    #print(labels)
    print("Accuracy for threshold " + str(threshold) + " : " + str(correct/201.0))


def fuzzy_sort(i, i_other, j, count, correlation):
    if patients[i][j] != "" and patients[i_other][j] != "":
        correlation += fuzz.token_sort_ratio(patients[i][j], patients[i_other][j])
        count += 1
    return count, correlation

def fuzzy_approach(patients, threshold):
    labels = [-1] * len(patients)
    group = 1
    group_st_ind = 0
    group_end_ind = 0
    for i in range(0, len(patients)):
        if i==0:
            labels[i] = group
            continue

        max_correlation = 0
        max_index = 0
        
        count = 0
        correlation = 0

        # calculate correlations

        # compare the names
        correlation += fuzz.token_sort_ratio(patients[i][3], patients[i-1][3])
        count += 1

        # compare the birthday
        correlation += fuzz.token_sort_ratio(patients[i][4], patients[i-1][4])
        count += 1

        # compare the sexes
        
        if patients[i][5] != "" and patients[i-1][5] != "":
            if (patients[i][5]).lower()[0] == (patients[i-1][5]).lower()[0]:
                correlation += 100
            count += 1

        # compare the addresses
        
        for j in range(6, 17):
            count, correlation = fuzzy_sort(i, i-1, j, count, correlation)
        '''
        ## current address 1
        # current address 2
        if patients[i][7] != "" and patients[i-1][7] != "":
            correlation += fuzz.token_sort_ratio(patients[i][7], patients[i-1][7])
            count += 1
        
        # current city
        if patients[i][8] != "" and patients[i-1][8] != "":
            correlation += fuzz.token_sort_ratio(patients[i][8], patients[i-1][8])
            count += 1

        # current state
        if patients[i][9] != "" and patients[i-1][9] != "":
            correlation += fuzz.token_sort_ratio(patients[i][9], patients[i-1][9])
            count += 1

        # current zipcode
        if patients[i][10] != "" and patients[i-1][10] != "":
            correlation += fuzz.token_sort_ratio(patients[i][10], patients[i-1][10])
            count += 1

        # previous name
        if patients[i][11] != "" and patients[i-1][11] != "":
            correlation += fuzz.token_sort_ratio(patients[i][11], patients[i-1][11])
            count += 1

        # compare the addresses
        # previous address 1
        if patients[i][12] != "" and patients[i-1][12] != "":
            correlation += fuzz.token_sort_ratio(patients[i][12], patients[i-1][12])
            count += 1
        # previous address 2
        if patients[i][13] != "" and patients[i-1][13] != "":
            correlation += fuzz.token_sort_ratio(patients[i][13], patients[i-1][13])
            count += 1
        
        # previous city
        if patients[i][14] != "" and patients[i-1][14] != "":
            correlation += fuzz.token_sort_ratio(patients[i][14], patients[i-1][14])
            count += 1

        # previous state
        if patients[i][15] != "" and patients[i-1][15] != "":
            correlation += fuzz.token_sort_ratio(patients[i][15], patients[i-1][15])
            count += 1

        # previous zipcode
        if patients[i][16] != "" and patients[i-1][16] != "":
            correlation += fuzz.token_sort_ratio(patients[i][16], patients[i-1][16])
            count += 1
        '''
        
        # print("Comparing " + str(max_correlation) + " and " + str(threshold))
        if correlation/count < threshold:
            group += 1
        
        labels[i] = group
    
    return labels


def fuzzy_approach_v2(patients, threshold):
    labels = [-1] * len(patients)
    group = 1

    for i in range(0, len(patients)):
        if i==0:
            labels[i] = group
            continue
        
        correlations = {}

        # calculate correlations
        for j in range(0, len(patients)):
            # compare the names
            if i == j:
                continue
            correlation = 0
            count = 0
            
            correlation += fuzz.token_sort_ratio(patients[i][3], patients[j][3])
            count += 1

            # compare the birthday
            correlation += fuzz.token_sort_ratio(patients[i][4], patients[j][4])
            count += 1

            # compare the sexes
            
            if patients[i][5] != "" and patients[j][5] != "":
                if (patients[i][5]).lower()[0] == (patients[j][5]).lower()[0]:
                    correlation += 100
                count += 1

            # compare the addresses
            
            for k in range(6, 17):
                count, correlation = fuzzy_sort(i, j, k, count, correlation)
            # print("Comparing " + str(max_correlation) + " and " + str(threshold))

            correlations[j] = correlation/count
        
        max_correlation = max(correlations.values())
        max_indices = list(filter(
            lambda x: x != -1, 
            [x if correlations[x] == max_correlation else -1 for x in correlations.keys()]))
        
        assoc_labels = [labels[m_ind] for m_ind in max_indices]

        if max_correlation >= threshold:
            f_l = list(filter(lambda x: x != -1, assoc_labels))
            inp_lab = group
            if f_l != []:
                inp_lab = f_l[0]

            for ind in max_indices:
                labels[ind] = inp_lab
            labels[i] = group

            if f_l == []:
                group += 1
        else:
            labels[i] = group
            group += 1

    return labels

patients = process()
threshold = 85
weights = [1,1,2,1,2,3,1,1,1,1]

labels = fuzzy_approach_v2(patients, threshold)
print(labels)
check_accuracy(patients, threshold, labels)
   

