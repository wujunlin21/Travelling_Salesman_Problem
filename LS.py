
import numpy as np
import math
import time

def LS_HillClimbing(fname, cutoff_time, seed):

    #set random seed as input
    np.random.seed(seed)

    #read data file of the input city
    fname=fname.split(".")[0]
    file_name="DATA/" + fname + ".tsp"
    map_file=open(file_name,'r')
    map_file.readline()
    map_file.readline()
    dimension=int(map_file.readline().split()[1])
    map_file.readline()
    map_file.readline()
    coord_array=np.zeros((dimension,2))
    for index in range(dimension):
        line=map_file.readline().split()
        city=int(line[0])
        coord_array[city-1,0]=float(line[1])
        coord_array[city-1,1]=float(line[2])

    #create distant array
    dist_array=np.zeros((dimension,dimension))
    for i in range(dimension):
        for j in range(i+1,dimension):
            distant=math.sqrt((coord_array[i][0]-coord_array[j][0])**2+(coord_array[i][1]-coord_array[j][1])**2 )
            dist_array[i,j]=distant
            dist_array[j,i]=distant

    


    #####################################################
    #Begin Hill-Climbing algorithm using 2-opt neiborhood

    #get start time
    start_time = time.time()
    total_time=0

    #Create initial city permutatoin
    city_order=np.random.permutation(range(1,dimension+1))
    city_order=np.append(city_order,np.array([city_order[0]]))
    #Get the cost of the initial city permutation
    total_cost=0
    for i in range(dimension):
        total_cost=total_cost+dist_array[city_order[i]-1,city_order[i+1]-1]
    
    #use trace_record to record the output for trace file
    trace_record=[]
    
    #Perform 2-opt swap until we get the lowest cost 
    while True:
        best_reduced=0
        #find the best neighbor (most decrease in dist)
        for i in range(dimension-2):
            for j in range(i+2,dimension):
                city_i=city_order[i]
                city_iplus=city_order[i+1]
                city_j=city_order[j]
                city_jplus=city_order[j+1]                
                orgin_dist=dist_array[city_i-1,city_iplus-1]+dist_array[city_j-1,city_jplus-1]
                reduced = orgin_dist-dist_array[city_i-1,city_j-1]-dist_array[city_iplus-1,city_jplus-1]
                if reduced>best_reduced:
                    best_reduced=reduced
                    best_i=i
                    best_j=j

        #Check if time within given cutoff time
        #if > cutoff time, stop hill-climbing
        time_len=time.time()-start_time
        if time_len>=cutoff_time:
            break 

        #Check if get 'best' cost, stop hill-climbing
        if best_reduced <= 0.000001:
            break
        
        #update city permutation
        temp=np.append(city_order[0:best_i+1],city_order[best_j:best_i:-1])
        temp=np.append(temp,city_order[best_j+1:])
        city_order=temp
        
        #calculate total cost of updated permutation
        total_cost=0
        for i in range(dimension):
            total_cost=total_cost+dist_array[city_order[i]-1,city_order[i+1]-1]

        #record improved solution
        trace_line="{:.3g}, {}\n".format(time_len,int(total_cost))
        trace_record.append(trace_line)
        total_time=time_len

    #write output file: trace
    trace_name=fname+"_LS2_"+str(cutoff_time)+"_"+str(seed)+".trace"
    trace_file=open("output/"+trace_name,"w")
    for line in trace_record:
        trace_file.write(line)
    trace_file.close()

    #write output file: solution
    soln_name=fname+"_LS2_"+str(cutoff_time)+"_"+str(seed)+".sol"
    soln_file=open("output/"+soln_name,"w")
    soln_file.write(str(int(total_cost))+"\n")
    for i in range(dimension):
        soln_line="{} {} {}\n".format(city_order[i]-1,city_order[i+1]-1,int(dist_array[city_order[i]-1,city_order[i+1]-1]))
        soln_file.write(soln_line)
    soln_file.close()

    #return quality of best solution, time used
    return int(total_cost),total_time

        
   

##if __name__ == '__main__':
    #file_names=["Boston.tsp","NYC"]
    #for filename in file_names:
        #best_soln=LS_HillClimbing(filename,600,1)

    
    
