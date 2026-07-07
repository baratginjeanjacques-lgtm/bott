import asyncio
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.errors import FloodWaitError, ChatWriteForbiddenError, RPCError
from datetime import datetime

api_id = 30642857
api_hash = "77e77669082c34aeff195c2db28c360f"
phone = "+33756830521"

SOURCE_CHANNEL = -1004293050467
MESSAGE_ID = 3

TARGET_GROUPS = [
    -1001762261954,
    -1001366416903,
    -1001426781373,
    -1001565333036,
    -1001877341618,
    -1002023584199,
    -1001439202411,
    -1001814884006,
    -1001577689719,
    -1001678591006,
    -1002113401020,
    -1001721042581,
    -1002013182086,
    -1001563129376,
    -1001604333686,
    -1001530741780,
]

DELAY = 3600
PAUSE_BETWEEN = 30

client = TelegramClient(MemorySession(), api_id, api_hash)

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def forward_loop():
    print("Connexion a Telegram...")
    await client.start(phone)
    print("Connecte avec succes !")
    print("\nDebut du transfert en boucle")
    print("- Source: FKSCanal")
    print("- Message ID: " + str(MESSAGE_ID))
    print("- " + str(len(TARGET_GROUPS)) + " groupes cibles")
    print("- Intervalle: " + str(DELAY) + "s (" + str(DELAY//60) + " minutes)")
    print("- Pause entre envois: " + str(PAUSE_BETWEEN) + "s")
    print("\n(Appuie sur CTRL+C pour arreter)\n")

    cycle = 0
    while True:
        cycle += 1
        now = get_time()
        print("\n" + "="*60)
        print("[" + now + "] Envoi CYCLE #" + str(cycle))
        print("="*60)
        
        success = 0
        failed = 0

        for i, group_id in enumerate(TARGET_GROUPS, 1):
            try:
                await client.forward_messages(group_id, MESSAGE_ID, SOURCE_CHANNEL)
                print("[" + str(i).zfill(2) + "/" + str(len(TARGET_GROUPS)) + "] OK Groupe " + str(group_id))
                success += 1
                await asyncio.sleep(PAUSE_BETWEEN)

            except FloodWaitError as e:
                print("[" + str(i).zfill(2) + "/" + str(len(TARGET_GROUPS)) + "] FLOODWAIT: " + str(e.seconds) + "s")
                await asyncio.sleep(e.seconds + 2)
                failed += 1

            except ChatWriteForbiddenError:
                print("[" + str(i).zfill(2) + "/" + str(len(TARGET_GROUPS)) + "] PAS ACCES")
                failed += 1

            except RPCError as e:
                print("[" + str(i).zfill(2) + "/" + str(len(TARGET_GROUPS)) + "] ERREUR RPC: " + str(e))
                failed += 1

            except Exception as e:
                print("[" + str(i).zfill(2) + "/" + str(len(TARGET_GROUPS)) + "] ERREUR: " + str(e))
                failed += 1

        print("="*60)
        print("Cycle " + str(cycle) + ": " + str(success) + " OK / " + str(failed) + " ERREURS")
        now = get_time()
        print("[" + now + "] Attente de " + str(DELAY) + "s (" + str(DELAY//60) + " min)")
        print("="*60 + "\n")
        
        await asyncio.sleep(DELAY)


if __name__ == "__main__":
    try:
        with client:
            client.loop.run_until_complete(forward_loop())
    except KeyboardInterrupt:
        print("\n\nScript arrete")
