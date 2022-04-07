from django.shortcuts import render
import time
import requests
from bs4 import BeautifulSoup
from .models import Contactform
from nsetools import nse


stock_list = []
lists = ["ACC","ADANIENT","ADANIGREEN","ADANIPORTS","ADANITRANS","ALKEM","AMBUJACEM","APOLLOHOSP","AUROPHARMA","DMART","BAJAJHLDNG","BANDHANBNK","BERGEPAINT","BIOCON","BOSCHLTD","CADILAHC","CIPLA","CHOLAFIN","COLPAL","DLF","DABUR","GAIL","GLAND","HAVELLS","HINDPETRO","ICICIGI","ICICIPRULI","IGL","INDUSTOWER","NAUKRI","INDIGO","JINDALSTEL","JUBLFOOD","LTI","LUPIN","MARICO","MUTHOOTFIN","NMDC","PIIND","PIDILITIND","PEL","PGHH","PNB","SBICARD","SIEMENS","SAIL","TORNTPHARM","MCDOWELLN","VEDL","YESBANK"]

def home(request):
    return render(request, 'home.html')

def search(request):

    key = []
    sales=[]
    expenses=[]
    oprofit=[]
    opm=[]
    oincome=[]
    intrest=[]
    Depreciation=[]
    pbt=[]
    tax=[]
    net=[]
    eps=[]

    keyshare= []
    sp1=[]
    sp2=[]
    sp3=[]
    sp4=[]
    sp5=[]

    keyratios= []
    debtor_days=[]
    inventory_days=[]
    days_payable=[]
    cash_conversion_cycle=[]
    working_capital_days=[]
    roc=[]

    key2= []
    sales2=[]
    expenses2=[]
    oprofit2=[]
    opm2=[]
    oincome2=[]
    intrest2=[]
    Depreciation2=[]
    pbt2=[]
    tax2=[]
    net2=[]
    eps2=[]
    divinded2=[]

    keyflow= []
    coa=[]
    cia= []
    cfa= []
    ncf= []

    keybalance= []
    bs1=[]
    bs2=[]
    bs3=[]
    bs4=[]
    bs5=[]
    bs6=[]
    bs7=[]
    bs8=[]
    bs9=[]
    bs10=[]
    detail=[]

    base_url="https://www.screener.in/company/"
    postf="/consolidated/"

    search_term = ''
    if 'search' in request.POST:
        search_term = request.POST['search']
        # print(search_term)

        for i in lists:
            if search_term == i:
                stock_list.insert(0, search_term)
                print(stock_list)

        url = base_url + search_term + postf
        r = requests.get(url)
        key, sales, expenses, oprofit, opm, oincome, intrest, Depreciation, pbt, tax, net, eps = insert_main(r)
        keyshare,sp1,sp2,sp3,sp4,sp5=insert_share(r)
        keyratios,debtor_days, inventory_days,days_payable,cash_conversion_cycle,working_capital_days,roc=insert_ratios(r)
        key2, sales2, expenses2, oprofit2, opm2, oincome2, intrest2, Depreciation2, pbt2, tax2, net2, eps2,divinded2 = insert_profit(r)
        keyflow,coa,cia,cfa,ncf=insert_cashflow(r)
        keybalance,bs1,bs2,bs3,bs4,bs5,bs6,bs7,bs8,bs9,bs10=insert_balance(r)
        detail=insert_detail(r)
        
        quater = {
            "search":search_term,
            "key" : key,
            "sales" : sales,
            "expenses" : expenses,
            "oprofit" : oprofit,
            "opm" : opm,
            "oincome" : oincome,
            "intrest" : intrest,
            "Depreciation" : Depreciation,
            "pbt" : pbt,
            "tax" : tax,
            "net" : net,
            "eps" : eps
        }
        share={
        "keyshare": keyshare,
        "sp1":sp1,
        "sp2":sp2,
        "sp3":sp3,
        "sp4":sp4,
        "sp5":sp5
        }
        ratios={
            "keyratios": keyratios,
            "debtor_days": debtor_days,
            "inventory_days": inventory_days,
            "days_payable": days_payable,
            "cash_conversion_cycle": cash_conversion_cycle,
            "working_capital_days": working_capital_days,
            "roc": roc
        }
        profit={
            "key2" : key2,
            "sales2" : sales2,
            "expenses2" : expenses2,
            "oprofit2" : oprofit2,
            "opm2" : opm2,
            "oincome2" : oincome2,
            "intrest2" : intrest2,
            "Depreciation2" : Depreciation2,
            "pbt2" : pbt2,
            "tax2" : tax2,
            "net2" : net2,
            "eps2" : eps2,
            "divinded2": divinded2
        }
        cashflow={
            "keyflow": keyflow,
            "coa": coa,
            "cia":cia,
            "cfa": cfa,
            "ncf": ncf
        }
        balance={
            "keybalance": keybalance,
            "bs1": bs1,
            "bs2": bs2,
            "bs3": bs3,
            "bs4": bs4,
            "bs5": bs5,
            "bs6": bs6,
            "bs7": bs7,
            "bs8": bs8,
            "bs9": bs9,
            "bs10": bs10
        }
        detail={
            "detail": detail
        }
        quater.update(share)
        quater.update(ratios)
        quater.update(profit)
        quater.update(cashflow)
        quater.update(balance)
        quater.update(detail)
    
    return render(request, 'search.html',quater)


# stock_list = ["ACC","ADANIENT"]


def insert_main(r):
    key= []
    sales=[]
    expenses=[]
    oprofit=[]
    opm=[]
    oincome=[]
    intrest=[]
    Depreciation=[]
    pbt=[]
    tax=[]
    net=[]
    eps=[]

    soup= BeautifulSoup(r.text,'html.parser')
    quarters=soup.find('section', id='quarters')

    key_length=0
    i=1
    k=1

    for stock_list in quarters.find_all('thead'):
        head=quarters.find_all('th')
        print(head)
        while(k <len(head)):
            key.insert(k,stock_list.find_all('th')[k].text)
            k=k+1  
        key_length=len(key)
        print(key_length)
    
    for s_info in quarters.find_all('tbody'):
        rows= s_info.find_all('tr')
        
        sal=1
        expen=key_length+2
        opr=key_length*2+3
        op=key_length*3+4
        oincm=key_length*4+5
        intr=key_length*5+6
        dep=key_length*6+7
        pb=key_length*7+8
        tx=key_length*8+9
        nt=key_length*9+10
        ep=key_length*10+11

            
        while(i<=key_length):
            sales.insert(sal,s_info.find_all('td')[sal].text)
            expenses.insert(expen,s_info.find_all('td')[expen].text)                
            oprofit.insert(opr,s_info.find_all('td')[opr].text)                
            opm.insert(op,s_info.find_all('td')[op].text)  
            oincome.insert(oincm,s_info.find_all('td')[oincm].text)  
            intrest.insert(intr,s_info.find_all('td')[intr].text)  
            Depreciation.insert(dep,s_info.find_all('td')[dep].text)  
            pbt.insert(pb,s_info.find_all('td')[pb].text)  
            tax.insert(tx,s_info.find_all('td')[tx].text)  
            net.insert(nt,s_info.find_all('td')[nt].text)  
            eps.insert(ep,s_info.find_all('td')[ep].text)  

            i=i+1
            sal=sal+1
            expen=expen+1
            opr=opr+1
            op=op+1
            oincm=oincm+1
            intr=intr+1
            dep=dep+1
            pb=pb+1
            tx=tx+1
            nt=nt+1
            ep=ep+1

    return key, sales, expenses, oprofit, opm, oincome, intrest, Depreciation, pbt, tax, net, eps


def insert_share(r):
    keyshare= []
    sp1=[]
    sp2=[]
    sp3=[]
    sp4=[]
    sp5=[]

    soup = BeautifulSoup(r.text,'html.parser')
    sholing=soup.find('section', id='shareholding')

    key_length=0
    i=1
    k=1
    
    for stock_list in sholing.find_all('thead'):
        head=sholing.find_all('th')
        print(head)
        print(len(head))
        while(k <len(head)):
            keyshare.insert(k,stock_list.find_all('th')[k].text)
            k=k+1  
        key_length=len(keyshare)
        print(key_length)
    
    for s_info in sholing.find_all('tbody'):
        rows= s_info.find_all('tr')
        
        s1=1
        s2=key_length+2
        s3=key_length*2+3
        s4=key_length*3+4
        s5=key_length*4+5
    
            
        while(i<=key_length):

            sp1.insert(s1,s_info.find_all('td')[s1].text)
            sp2.insert(s2,s_info.find_all('td')[s2].text)                
            sp3.insert(s3,s_info.find_all('td')[s3].text)                
            sp4.insert(s4,s_info.find_all('td')[s4].text)
            if(len(rows)==5):  
                sp5.insert(s5,s_info.find_all('td')[s5].text)  
            else:
                sp5.insert(s5,0)

            i=i+1
            s1=s1+1
            s2=s2+1
            s3=s3+1
            s4=s4+1
            s5=s5+1
        
    return keyshare,sp1,sp2,sp3,sp4,sp5

def insert_ratios(r):

    # Define List For Store The Scrap Data

    keyratios= []
    debtor_days=[]
    inventory_days=[]
    days_payable=[]
    cash_conversion_cycle=[]
    working_capital_days=[]
    roc=[]

    # Finding Section Using Web Scrap

    soup= BeautifulSoup(r.text,'html.parser')
    ratios= soup.find('section', id='ratios')

    key_length=0
    i=1
    k=1

    # This Loop For Finding the head of particular section means its found year

    for stock_list in ratios.find_all('thead'):
        head=ratios.find_all('th')
        print(head)
        while(k < len(head)):
            keyratios.insert(k,stock_list.find_all('th')[k].text)
            k=k+1  
            print(keyratios)
        key_length=len(keyratios)
        # print(key_length)
    
    # This Loop For Findind Data Of Section 

    for s_info in ratios.find_all('tbody'):
        rows= s_info.find_all('tr')
        i=1
        id=key_length+2
        dp=key_length*2+3
        cc=key_length*3+4
        wd=key_length*4+5
        ro=key_length*5+6
        
        # its run when length of key is less than I

        while(i<=key_length):
            debtor_days.insert(i,s_info.find_all('td')[i].text)
            inventory_days.insert(id,s_info.find_all('td')[id].text)                
            days_payable.insert(dp,s_info.find_all('td')[dp].text)                
            cash_conversion_cycle.insert(cc,s_info.find_all('td')[cc].text)  
            working_capital_days.insert(wd,s_info.find_all('td')[wd].text)  
            roc.insert(ro,s_info.find_all('td')[ro].text)  

            dp=dp+1
            id=id+1
            i=i+1
            cc=cc+1
            wd=wd+1
            ro=ro+1
        return keyratios,debtor_days,inventory_days,days_payable,cash_conversion_cycle,working_capital_days,roc


def insert_profit(r):
    soup= BeautifulSoup(r.text,'html.parser')
    profitloss=soup.find('section', id='profit-loss')

    key2= []
    sales2=[]
    expenses2=[]
    oprofit2=[]
    opm2=[]
    oincome2=[]
    intrest2=[]
    Depreciation2=[]
    pbt2=[]
    tax2=[]
    net2=[]
    eps2=[]
    divinded2=[]


    key_length=0
    i=1
    k=1

    for s_info in profitloss.find_all('thead'):
        head=s_info.find_all('th')
        while(k<len(head)):
            key2.insert(k,s_info.find_all('th')[k].text)
            k=k+1
    print(key2)
    key_length=len(key2)
    
    for s_info in profitloss.find_all('tbody'):
        rows= s_info.find_all('tr')
        
        sal=1
        expen=key_length+2
        opr=key_length*2+3
        op=key_length*3+4
        oincm=key_length*4+5
        intr=key_length*5+6
        dep=key_length*6+7
        pb=key_length*7+8
        tx=key_length*8+9
        nt=key_length*9+10
        ep=key_length*10+11
        dp=key_length*11+12

            
        while(i<=key_length):
            sales2.insert(sal,s_info.find_all('td')[sal].text)
            expenses2.insert(expen,s_info.find_all('td')[expen].text)                
            oprofit2.insert(opr,s_info.find_all('td')[opr].text)                
            opm2.insert(op,s_info.find_all('td')[op].text)  
            oincome2.insert(oincm,s_info.find_all('td')[oincm].text)  
            intrest2.insert(intr,s_info.find_all('td')[intr].text)  
            Depreciation2.insert(dep,s_info.find_all('td')[dep].text)  
            pbt2.insert(pb,s_info.find_all('td')[pb].text)  
            tax2.insert(tx,s_info.find_all('td')[tx].text)  
            net2.insert(nt,s_info.find_all('td')[nt].text)  
            eps2.insert(ep,s_info.find_all('td')[ep].text)  
            divinded2.insert(dp,s_info.find_all('td')[dp].text)

            i=i+1
            sal=sal+1
            expen=expen+1
            opr=opr+1
            op=op+1
            oincm=oincm+1
            intr=intr+1
            dep=dep+1
            pb=pb+1
            tx=tx+1
            nt=nt+1
            ep=ep+1
            dp=dp+1
    return key2, sales2, expenses2, oprofit2, opm2, oincome2, intrest2, Depreciation2, pbt2, tax2, net2, eps2,divinded2

def insert_cashflow(r):
    keyflow= []
    coa=[]
    cia= []
    cfa= []
    ncf= []

    soup= BeautifulSoup(r.text,'html.parser')
    cashflow=soup.find('section', id='cash-flow')

    key_length=0
    i=1
    k=1

    for stock_list in cashflow.find_all('thead'):
        head=cashflow.find_all('th')
        while(k <len(head)):
            keyflow.insert(k,stock_list.find_all('th')[k].text)
            k=k+1  
        key_length=len(keyflow)
        print(key_length)
    
    for s_info in cashflow.find_all('tbody'):
        rows= s_info.find_all('tr')
        
        cc1=1
        cc2=key_length+2
        cc3=key_length*2+3
        cc4=key_length*3+4
         
        while(i<=key_length):
            coa.insert(cc1,s_info.find_all('td')[cc1].text)
            cia.insert(cc2,s_info.find_all('td')[cc2].text)                
            cfa.insert(cc3,s_info.find_all('td')[cc3].text)                
            ncf.insert(cc4,s_info.find_all('td')[cc4].text)  
        
            i=i+1
            cc1=cc1+1
            cc2=cc2+1
            cc3=cc3+1
            cc4=cc4+1

    return keyflow,coa,cia,cfa,ncf

def insert_balance(r):
    keybalance= []
    bs1=[]
    bs2=[]
    bs3=[]
    bs4=[]
    bs5=[]
    bs6=[]
    bs7=[]
    bs8=[]
    bs9=[]
    bs10=[]

    soup= BeautifulSoup(r.text,'html.parser')
    balancesheet=soup.find('section', id='balance-sheet')

    key_length=0
    i=1
    k=1

    for stock_list in balancesheet.find_all('thead'):
        head=balancesheet.find_all('th')
        print(head)
        while(k <len(head)):
            keybalance.insert(k,stock_list.find_all('th')[k].text)
            k=k+1  
        key_length=len(keybalance)
        print(key_length)
    
    for s_info in balancesheet.find_all('tbody'):
        rows= s_info.find_all('tr')
        
        b1=1
        b2=key_length+2
        b3=key_length*2+3
        b4=key_length*3+4
        b5=key_length*4+5
        b6=key_length*5+6
        b7=key_length*6+7
        b8=key_length*7+8
        b9=key_length*8+9
        b10=key_length*9+10

            
        while(i<=key_length):
            bs1.insert(b1,s_info.find_all('td')[b1].text)
            bs2.insert(b2,s_info.find_all('td')[b2].text)                
            bs3.insert(b3,s_info.find_all('td')[b3].text)                
            bs4.insert(b4,s_info.find_all('td')[b4].text)  
            bs5.insert(b5,s_info.find_all('td')[b5].text)  
            bs6.insert(b6,s_info.find_all('td')[b6].text)  
            bs7.insert(b7,s_info.find_all('td')[b7].text)  
            bs8.insert(b8,s_info.find_all('td')[b8].text)  
            bs9.insert(b9,s_info.find_all('td')[b9].text)  
            bs10.insert(b10,s_info.find_all('td')[b10].text)  

            i=i+1
            b1=b1+1
            b2=b2+1
            b3=b3+1
            b4=b4+1
            b5=b5+1
            b6=b6+1
            b7=b7+1
            b8=b8+1
            b9=b9+1
            b10=b10+1

    return keybalance,bs1,bs2,bs3,bs4,bs5,bs6,bs7,bs8,bs9,bs10

def insert_detail(r):
    detail=[]
    i=0
    soup= BeautifulSoup(r.text,'html.parser')
    basic_detail=soup.find('div', class_="company-ratios")

    for s_info in basic_detail.find_all('ul',id="top-ratios"):
        rows= s_info.find_all('li')
        data=s_info.find_all('span',class_="number")
        # print(data)
        while(i<len(data)):
            detail.insert(i,s_info.find_all('span',class_="number")[i].text)
            i=i+1
        # print(data)
        print(detail)

    len_detail=len(detail)
    return detail

def about(request):
    return render(request, 'about.html')

def contact(request):
    if (request.method == 'POST'):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('msg', '')

        contact = Contactform(name=name, email=email, message=message)
        contact.save()
    return render(request, 'contact.html')  