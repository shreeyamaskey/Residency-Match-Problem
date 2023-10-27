'''
ResidencyMatch.py

This algorithm operates by reading an input file of the form

[residents | hospitals] preference 1, preference 2, preference 3, preference 4, ...

Any whitespace occurring in the input files is stripped off.

Usage:

    python ResidencyMatch.py [residents preference file] [hospitals preference file]

[Shreeya Maskey]

'''

import sys
import csv

class ResidencyMatch:

    # behaves like a constructor
    def __init__(self):
        '''
        Think of
        
            unmatchedHospitals
            residentsMappings
            hospitalsMappings
            matches
            
        as being instance data for your class.
        
        Whenever you want to refer to instance data, you must
        prepend it with 'self.<instance data>'
        '''
        
        # list of unmatched hospitals
        self.unmatchedHospitals = [ ]

        # list of unmatched residents
        self.unmatchedResidents = [ ]
        
        # dictionaries representing preferences mappings
        
        self.residentsMappings = { }
        self.hospitalsMappings = { }
        
        # dictionary of matches where mapping is resident:hospital
        self.matches = { }
        
        # read in the preference files
        
        '''
        This constructs a dictionary mapping a resident to a list of hospitals in order of preference
        '''
        
        prefsReader = csv.reader(open (sys.argv[1],'r'), delimiter = ',')
        for row in prefsReader:
            resident = row[0].strip()

             # all hospitals are initially unmatched
            self.unmatchedResidents.append(resident)

            # maps a resident to a list of preferences
            self.residentsMappings[resident] = [x.strip() for x in row[1:]]
            
            # initially have each resident as unmatched
            self.matches[resident] = None
        
        '''
        This constructs a dictionary mapping a hospital to a list of residents in order of preference
        '''
        
        prefsReader = csv.reader(open (sys.argv[2],'r'), delimiter = ',')
        for row in prefsReader:
            
            hospital = row[0].strip()
            
            # all hospitals are initially unmatched
            self.unmatchedHospitals.append(hospital)
            
            # maps a resident to a list of preferences
            self.hospitalsMappings[hospital] = [x.strip() for x in row[1:]] 
    
    # print out the stable match
    def reportMatches(self):
        print('Here are the final matches')
        print(self.matches)
            
    # follow the chart described in the lab to find the stable match
    def runMatch(self):
        '''
        It is suggested you use the debugger or similar output statements
        to determine what the contents of the data structures are
        '''
        while self.unmatchedHospitals:
            current_hosp = self.unmatchedHospitals[0] # current hospital in question will always be the first in the list
            hosp_want = (self.hospitalsMappings[current_hosp][0]) # the resident hospital prefers the most
            if hosp_want in self.unmatchedResidents:
                self.matches[hosp_want] = current_hosp # Put the tentative match in the dictionary
                self.unmatchedHospitals.pop(0) # Remove resident from unmatched list
                res_index = self.unmatchedResidents.index(hosp_want)
                self.unmatchedResidents.pop(res_index) # Remove hospital from unmatched list
                # Remove resident from hospitals preference list
                self.hospitalsMappings[current_hosp].remove(hosp_want)
            else:
                res_pref_matched = self.matches[hosp_want]
                matched_index = self.residentsMappings[hosp_want].index(res_pref_matched) # index of the already matched hospital
                curr_index = self.residentsMappings[hosp_want].index(current_hosp) # index of the current hospital in resident's list
                # if matched index is greater than current index;
                # match current resident and hospital and then append the previously matched resident to unmatched list
                # and remove the resident from the hospital's list
                if matched_index > curr_index:
                    self.matches[hosp_want] = current_hosp
                    self.unmatchedHospitals.append(res_pref_matched)
                    self.hospitalsMappings[current_hosp].remove(hosp_want)
                self.unmatchedHospitals.pop(0)
                #if matched index is less than current index;
                # current resident remains unmatched, and we remove the resident from hospital's list
                if matched_index < curr_index:
                    self.unmatchedHospitals.append(current_hosp)
                    self.hospitalsMappings[current_hosp].remove(hosp_want)


if __name__ == "__main__":
   
    # some error checking
    if len(sys.argv) != 3:
        print('ERROR: Usage\n python ResidencyMatch.py [residents preferences] [hospitals preferences]')
        quit()

    # create an instance of ResidencyMatch 
    match = ResidencyMatch()

    # now call the runMatch() function
    match.runMatch()
    
    # report the matches
    match.reportMatches()



