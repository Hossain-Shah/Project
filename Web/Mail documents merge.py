from mailmerge import MailMerge
from datetime import date
template = "Mail Merge.docx"
document = MailMerge(template)
print(document.get_merge_fields())
document.merge(
    status='Promoted',
    city='Dhaka',
    phone_number='01521102074',
    Occupation='Software Engineer',
    zip='1207',
    compensation='$25000',
    state='BD',
    address='Kazi Nazrul Islam Road',
    date='{:%d-%b-%Y}'.format(date.today()),
    recipient='Anindo')

document.write('output.docx')
