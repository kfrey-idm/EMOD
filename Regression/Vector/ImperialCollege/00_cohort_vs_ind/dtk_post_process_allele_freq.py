import json
import sys, os


def GetColumnIndexesFromHeader( header ):
    used_columns = []
    used_columns.append( "Time"             )
    used_columns.append( "NodeID"           )
    used_columns.append( "Genome"           )
    used_columns.append( "VectorPopulation" )
    used_columns.append( "STATE_INFECTIOUS" )
    used_columns.append( "STATE_INFECTED"   )
    used_columns.append( "STATE_ADULT"      )
    used_columns.append( "STATE_MALE"       )
    used_columns.append( "STATE_IMMATURE"   )
    used_columns.append( "STATE_LARVA"      )
    used_columns.append( "STATE_EGG"        )

    header = header.replace('\n','')
    header_array = header.split( ',' )
    col_indexes_map = {}
    for index in range( len( header_array ) ):
        ch = header_array[ index ].strip()
        for used in used_columns:
            if ch.startswith( used ):
                col_indexes_map[ used ] = index
                break
    return col_indexes_map
    
# --------------------------------------------------------------
# Read the file produced by ReportVectorGenetics.cpp and return
# a list of GenomeData objects representing each line/genome
# --------------------------------------------------------------
def ReadData( filename ):
    data_map = {}
    prev_time = 0.0
    with open( filename, "r" ) as rs:
        header = rs.readline() # chew up header
        col_indexes_map = GetColumnIndexesFromHeader( header )
        for line in rs:
            line = line.replace('\n','')
            line_array = line.split( ',' )

            if len(line_array) == len(col_indexes_map):
                genome = line_array[ col_indexes_map["Genome"] ]
                data = float(   line_array[ col_indexes_map["VectorPopulation"] ])

                if genome not in data_map.keys():
                    data_map[ genome ] = []
                    
                data_map[ genome ].append( data )

    return data_map

def CalculateAlleleFrequency( allele_list, genome_to_data_map ):
    genome_list = list( genome_to_data_map )
    num_pts = len( genome_to_data_map[ genome_list[0] ] )
 
    allele_to_frequency_map = {}
    for allele in allele_list:
        allele_to_frequency_map[ allele ] = []
    
    for i in range(num_pts):
        total = 0
        for genome in genome_list:
            total += genome_to_data_map[ genome ][i]
        for allele in allele_list:
            total_with_allele = 0
            for genome in genome_list:
                gamete_array = genome.split( ':' )
                if allele in gamete_array[0]:
                    total_with_allele += genome_to_data_map[ genome ][ i ]
                if allele in gamete_array[1]:
                    total_with_allele += genome_to_data_map[ genome ][ i ]
            if total > 0.0:
                allele_to_frequency_map[ allele ].append( total_with_allele/(2*total) )
            else:
                allele_to_frequency_map[ allele ].append( 0 )
                
    return allele_to_frequency_map
    
    
def WriteData( filename, name_to_data_map ):
    if len(name_to_data_map) == 0:
        return;
        
    name_list = list( name_to_data_map.keys() )
    num_pts = len( name_to_data_map[ name_list[0] ] )
    
    with open( filename, "w" ) as output:
        # write header
        output.write("Time")
        for name in name_list:
            output.write(","+name)
        output.write("\n")
        
        for i in range(num_pts):
            output.write(str(i))
            for name in name_list:
                output.write(","+str( name_to_data_map[ name ][i]) )
            output.write("\n")


def application( output_path ):

    config_json = json.loads( open( "config.json" ).read() )["parameters"]
    run_number = config_json["Run_Number"]

    allele_list = []
    allele_list.append( "a0" )
    allele_list.append( "a1" )
    allele_list.append( "a2" )
    allele_list.append( "a3" )
    allele_list.append( "b0" )
    allele_list.append( "b1" )
    allele_list.append( "b2" )
    allele_list.append( "b3" )
    
    input_filename = os.path.join( output_path, "ReportVectorGenetics_arabiensis_GENOME.csv" )
    
    genome_data_map = ReadData( input_filename )
    allele_to_frequency_map = CalculateAlleleFrequency( allele_list, genome_data_map )
    
    results_dir = "../../cohort_vs_ind/results"
    #results_dir = output_path
    if not os.path.exists( results_dir ):
        os.makedirs( results_dir )
    
    filename = "AlleleFrequency_" + str(run_number) + ".csv"
    full_filename = os.path.join( results_dir, filename )
    WriteData( full_filename, allele_to_frequency_map )
    
    print("Done creating Allele Frequency")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need output path")
        exit(0)

    output_path = sys.argv[1]

    application( output_path )