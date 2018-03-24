from tkinter import *
from tkinter import ttk


def label(row, column, text):
    L = Label(root, text=text, anchor='w')
    L.grid(row=row,column=column,sticky="nw",pady=2,padx=3)


def button(root, row, column, text, command):
    B = Button(root, text=text, command=command, width=15)
    B.grid(row=row, column=column, sticky="e", pady=4, padx=3)


def entry(row, column, insert="", show=""):
    E = Entry(root, width=32)
    E.insert(0, insert)
    E.config(show=show)
    E.grid(row=row,column=column)
    return E


def show_ldif():

    values_list = []
    givenname = var0.get()
    sn = var1.get()
    country = var2.get()
    location = var3.get()
    skype = var8.get()

    cn = givenname[0].lower() + sn.lower()
    email = cn + "@company.com"

    # ldif is import format for openLDAP
    ldif_list =[]
    ldif_list.append(("dn: cn=%s,cn=people,ou=company,dc=company,dc=com\n") % cn)
    ldif_list.append('c: %s\n'% country)
    ldif_list.append('cn: %s\n'% cn)
    ldif_list.append(('objectclass: inetOrgPerson\n'
                      'objectclass: posixAccount\n'
                      'objectclass: top\n'
                      'objectclass: shadowAccount\n'
                      'objectclass: ldapPublicKey\n'
                      'objectclass: extensibleObject\n'))

    ldif = ''.join(ldif_list)

    top = Toplevel()
    top.title("Result")

    ldif_text = Text(top, height=30, width=50)
    ldif_text.insert(END, ldif)
    ldif_text.grid(row=0,column=0,columnspan = 2)

    button(top, 1, 1, "Copy to Clipboard", yes_no)
    button(top, 1, 0, "Import to LDAP", yes_no)


def yes_no():
    pass


root = Tk()

root.style = ttk.Style()
root.style.theme_use("clam")

root.title("LDAP Adder")

label(0, 0, 'First name')
var0 = entry(0, 1)

label(1, 0, 'Second name')
var1 = entry(1, 1)

label(2, 0, 'Country (two letters)')
var2 = entry(2, 1)

label(3, 0, 'City')
var3 = entry(3, 1)

label(8, 0, 'Skype')
var8 = entry(8, 1)

label(13, 0, '')

button(root, 14, 0, 'Show', show_ldif)
button(root, 14, 1, 'Quit', root.quit)

root.mainloop()

