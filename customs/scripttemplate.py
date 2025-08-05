from datahandler import Levelling
userdata = Levelling()

def main(recipientid, channelid):
    print(f"{recipientid} bought an item in {channelid} and triggered this script! Granting them 100XP..")
    userdata.addxp(recipientid, 100)