"""
Tests for parsing netfile form 460A data.
Some metadata:
^ calculated_Amount: None, -294.84,-200.0,50.0,99.0,100.0
x calculated_Date: None, 2015-01-07T00:00:00.0000000-08
^ cmte_Id        : Committee ID # (If [COM|RCP] &, nan,#890268,1244975,1264568
^ entity_Cd      : Contributor Type of Entity (In, COM,IND,OTH,SCC
^ filerId        : None, COA-113952,COA-113968,COA-1139
^ filerName      : None, Better Transportation for Alam
x filingId       : None, 155104080,155521798,155524068,
x intr_City      : Intermediary City, nan,Alameda
x intr_NamL      : Intermediary Last Name, nan,Wilma Chan For Supervisor
x intr_ST        : Intermediary State, nan,CA
x intr_Zip4      : Intermediary Zip, nan,94501
x netFileKey     : None, 00bab3072253498da017a4e60105ea
^ tran_Amt1      : Transaction Amount, -200.0,-294.84,100.0,1000.0,10
^ tran_Amt2      : Cumulative Year-To-Date, -6867.12,0.0,100.0,1000.0,101.
tran_City      : Transaction Entity's City, Alameda,Alamo,Arcata,Atherton,
tran_Date      : Transaction Date, 2015-01-07T00:00:00.0000000-08
tran_Date1     : Transaction Date (if a range), 2013-10-03T00:00:00.0000000-07
tran_Emp       : Transaction Entity's Employer, nan,ABCO Wire & Metal Products
tran_Id        : Transaction ID # (not necessar, 1DOCUB61ZGyZ,21mtbGMusZdR,22Lp
tran_NamF      : Transaction Entity's First Nam, nan,Albert,Alice,Andrew,Andy,A
tran_NamL      : Transaction Entity's Last Name, ABC Security  Service Inc,ACME
tran_Occ       : Transaction Entity's Occupatio, nan,Actuary,Acupuncturist,Acup
tran_ST        : None, CA,MO,TX
tran_Type      : Transaction Type (T=Third Part, nan,R,X
tran_Zip4      : Transaction Entity's Zip Code, 63105,75702,75711,90036,90040,
"""
