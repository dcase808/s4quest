from stellar_sdk import *


server = Server("https://horizon.stellar.org")

alb = Keypair.from_secret("SEKRETNASPERMA")

base_fee = "1000"

accs = [
    "GDZPC43BX4VUTIQSYV4WNTDYDBEX27EKK55VIGFBY7GKUSKCKMRELUWL",
    "GAHY6P4UWHVS4U2PI24RGMFOPN77RCGJT5CENPJOI3SZXP6FHN7TYOCU",
    "SPERMA",
    "CIPA"
]

for y in accs:
    
    ids = (server.claimable_balances().for_claimant(y).limit(200).call())["_embedded"]["records"]
    
    id_list = []
    
    for x in ids:
        id_list.append(x["id"])
    
    source_acc = server.load_account(y)
    base_fee = server.fetch_base_fee()
    
    transaction = (
        TransactionBuilder(
            source_account=source_acc,
            network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
    )
    
    for x in id_list:
        transaction.append_claim_claimable_balance_op(x)
    
    transaction.append_account_merge_op(alb.public_key)
    
    transaction = transaction.build()
    
    transaction.sign(alb)

    print(transaction.to_xdr())
    
    print(server.submit_transaction(transaction))
