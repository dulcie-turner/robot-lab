#Import necessary libraries and modules
import csv

#Open the CSV file and write the header row to the CSV file
csvfile_w=open('logger.csv', 'w', newline='')
writer = csv.DictWriter(csvfile_w, fieldnames=['number','data'])
writer.writeheader()  

#Write data to the CSV file
count=0    
data=20
writer.writerow({'number':count,'data':data})  

#Close the CSV file
csvfile_w.close()





