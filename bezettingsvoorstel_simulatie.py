#simulatie bezettingsvoorstel puntentelling (POST prinsenbeek als use-case)

import random
import csv
from operator import itemgetter

AANTAL_UITRUKKEN = 100;
aantalKeerOnderbezet = 0;
aantalKeerTS6 = 0;
aantalKeerTS4 = 0;

#Array Naam, Opkomstpercentage, Bevelvoerder, #BV uitrukken, Chauffeur, #Chauf uitrukken, Manschap, #Manschap uitrukken, #Aantal keren opgekomen
post = [
    ["vrw1", 0.71, None, None, None, None, 0.0, 0.0, 0], 
    ["vrw2", 0.18, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw3", 0.53, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw4", 0.3, None, None, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw5", 0.6, 0.0, 0.0, None, None, 0.0, 0.0, 0],
    ["vrw6", 0.67, None, None, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw7", 0.41, 0.0, 0.0, None, None, 0.0, 0.0, 0],
    ["vrw8", 0.3, None, None, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw9", 0.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw10", 0.63, None, None, None, None, 0.0, 0.0, 0],
    ["vrw11", 0.84, None, None, None, None, 0.0, 0.0, 0],
    ["vrw12", 0.88, 0.0, 0.0, None, None, 0.0, 0.0, 0],
    ["vrw13", 0.49, None, None, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw14", 0.44, None, None, None, None, 0.0, 0.0, 0],
    ["vrw15", 0.87, None, None, None, None, 0.0, 0.0, 0],
    ["vrw16", 0.68, None, None, None, None, 0.0, 0.0, 0],
    ["vrw17", 0.2, None, None, 0.0, 0.0, 0.0, 0.0, 0],
    ["vrw18", 0.58, None, None, None, None, 0.0, 0.0, 0],
] 

def reactieMelding(person):
    return random.randrange(100) < person[1]*100
    
def filterOpgekomenFuncties(opkomst, function):
    byFunctie = [];
    for person in opkomst:
        if(function == "bv" and person[2] != None and person[1]):
            byFunctie.append(person);
        if(function == "ch" and person[4] != None and person[1]):
            byFunctie.append(person);
        if(function == "ma" and person[6] != None and person[1]):
            byFunctie.append(person);
    return byFunctie;

def printPersonen(opkomstFunctie):
    for f in opkomstFunctie:
        print(f); 
    print ("---------------");   

def puntenToekennenNietIngedeeld(opkomst , bvIngedeeld, chIngedeeld, masIngedeeld):
    nietIngedeeldePersonen = opkomst;
    #punten toekennen aan niet ingedeelde personen
    for person in nietIngedeeldePersonen:
        if(person[0] == bvIngedeeld[0]):
            nietIngedeeldePersonen.remove(person);
    
    for person in nietIngedeeldePersonen:
        if(person[0] == chIngedeeld[0]):
            nietIngedeeldePersonen.remove(person);
          
    nietIngedeeldePersonen = [x for x in nietIngedeeldePersonen if x not in masIngedeeld]          
    
    #punten toekennen
    for person in nietIngedeeldePersonen:
        print("niet ingedeeld: "+person[0]);
        for postVrw in post:
            if(person[0] == postVrw[0]):
                aantalFuncties = 1;
                if(postVrw[2] != None):
                   aantalFuncties+=1; 
                if(postVrw[4] != None):
                   aantalFuncties+=1; 
                
                if(postVrw[2] != None):
                    postVrw[2] = postVrw[2] - (1/aantalFuncties);
                if(postVrw[4] != None):
                    postVrw[4] = postVrw[4] - (1/aantalFuncties);
                if(postVrw[6] != None):
                    postVrw[6] = postVrw[6] - (1/aantalFuncties);
                    
    print("----------");
                    
def puntenCorrigerenWelIngedeeld(bvIngedeeld, chIngedeeld, masIngedeeld):
    for postVrw in post:
        if(bvIngedeeld[0] == postVrw[0]):
            postVrw[2] = 0;
        if(chIngedeeld[0] == postVrw[0]):
            postVrw[4] = 0;
            
        for ma in masIngedeeld:
            if(ma[0] == postVrw[0]):
                postVrw[6] = 0;

def puntenToekennen(opkomst , bvIngedeeld, chIngedeeld, masIngedeeld):
    puntenToekennenNietIngedeeld(opkomst , bvIngedeeld, chIngedeeld, masIngedeeld);
    puntenCorrigerenWelIngedeeld(bvIngedeeld, chIngedeeld, masIngedeeld);
 
def uitrukkenToevoegen(bvIngedeeld, chIngedeeld, masIngedeeld):
    for postVrw in post:
        if(bvIngedeeld[0] == postVrw[0]):
            postVrw[3] += 1;
        if(chIngedeeld[0] == postVrw[0]):
            postVrw[5] += 1;
            
        for ma in masIngedeeld:
            if(ma[0] == postVrw[0]):
                postVrw[7] += 1;
    
   
def resultatenNaarCSV():
    #Naam, Opkomstpercentage, Bevelvoerder, #BV uitrukken, Chauffeur, #Chauf uitrukken, Manschap, #Manschap uitrukken, #Aantal keren opgekomen
    header = ['naam', 'opkomstpercentage', 'bvUitrukken', 'chauffeurUitrukken', 'manschapUitrukken', 'kerenOpgekomen']
    
    with open('resultatenSimilatie_enkel.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter=';')

        # write the header
        writer.writerow(header)

        for person in post:
        # write the data
           writer.writerow([person[0], person[1], person[3], person[5], person[7], person[8]])
    
def maakBezetting(opkomst):
    bvs = filterOpgekomenFuncties(opkomst, "bv");
    chs = filterOpgekomenFuncties(opkomst, "ch");
    mas = filterOpgekomenFuncties(opkomst, "ma");
      
    #printPersonen(bvs);
    #printPersonen(chs);
    #printPersonen(mas);

    #Er moet altijd 1 BV zijn en 1 CH en 2 of 4 manschappen. (Precom deelt geen TS5 in)
    if(len(bvs) == 0):
        return False;
    if (len(chs) == 0):
        return False;
    # Enige BV en enige CH is dezelfde persoon
    if (len(bvs) == 1 and len(chs) == 1 and bvs[0] == chs[0]) :
       return False;
       
    #kies bv, ch en ma obv punten
    sortedBvs = sorted(bvs, key=itemgetter(2))
    sortedChs = sorted(chs, key=itemgetter(4))
    sortedMas = sorted(mas, key=itemgetter(6))
    
    #print("gesorteerd:")
    #for p in sortedBvs:
    #    print(p[0]);
    #print("----");
    #for p in sortedChs:
    #    print(p[0]);
    #print("----");
    #for p in sortedMas:
    #    print(p[0]);
    #print("----");
    
    bvIngedeeld = sortedBvs[:1][0];
    chIngedeeld = sortedChs[:1][0];
         
    if(sortedBvs[:1][0] == sortedChs[:1][0] and len(sortedChs) > 1):
        bvIngedeeld = sortedBvs[0]
        chIngedeeld = sortedChs[1]
    
    elif(sortedBvs[:1][0] == sortedChs[:1][0] and len(sortedBvs) > 1):
        bvIngedeeld = sortedBvs[1]
        chIngedeeld = sortedChs[0]
        
    #printPersonen([sortedBvs]);
    #printPersonen([sortedChs]);
    #printPersonen([sortedMas]);
    
    for person in sortedMas:
        if(person[0] == bvIngedeeld[0]):
            sortedMas.remove(person);
    
    for person in sortedMas:
        if(person[0] == chIngedeeld[0]):
            sortedMas.remove(person);
    
    if(len(sortedMas) >= 4):
        #TS6
            masIngedeeld = sortedMas[:4];
            global aantalKeerTS6;
            aantalKeerTS6+=1;
            
    elif(len(sortedMas) >= 2):
        #TS4
            masIngedeeld = sortedMas[:2];
            global aantalKeerTS4;
            aantalKeerTS4+=1;
    else:
        #te weinig manschappen opgekomen
        return False;
    
    print("Bezettingsvoorstel:");
    print("-------------------------:");
    print("Bevelvoerder:");
    print(bvIngedeeld[0]);
    print("Chauffeur:");
    print(chIngedeeld[0]);
    print("Manschappen:");
    for ma in masIngedeeld:
        print(ma[0]);
    print("-------------------------:");
    
    puntenToekennen(opkomst , bvIngedeeld, chIngedeeld, masIngedeeld);
    uitrukkenToevoegen(bvIngedeeld, chIngedeeld, masIngedeeld);
    return True;
    
for uitruk in range(AANTAL_UITRUKKEN):
    print("------------------------");
    print("Uitruk nr: "+str(uitruk+1))
  
    opkomst = [];
    for person in post:
        if(reactieMelding(person)):
            print("opgekomen: "+person[0]);
            opkomst.append(person)
            for vrw in post:
                if(vrw[0] == person[0]):
                    vrw[8] += 1;
    
    bezettingGemaakt = maakBezetting(opkomst);
    if not bezettingGemaakt:
        aantalKeerOnderbezet+=1;
    print(post);
       
    #for reactie in opkomst:
    #  print(reactie);

resultatenNaarCSV();

print("\n");
print("--------------------------");
print("Aantal keer TS4: "+str(aantalKeerTS4));
print("Aantal keer TS6: "+str(aantalKeerTS6));
print("Aantal keer onderbezet: "+str(aantalKeerOnderbezet));
  
