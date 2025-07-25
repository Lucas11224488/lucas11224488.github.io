import numpy as np
import random
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure your HTML file is named 'index.html' and in a 'templates' folder.

@app.route('/submit_players', methods=['POST'])
def submit_players():
    data = request.get_json()
    LeftPlayer = data.get('LeftPlayer')
    RightPlayer = data.get('RightPlayer')
    print("LeftPlayer:", LeftPlayer)
    Result = MainFight(LeftPlayer, RightPlayer)
    return jsonify({"output": Result})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# LItems = ["BlacksmithBond", "BrittlebarkArmor", "BlacksmithBond"]
# RItems = ["VampireWine", "DoublePlatedArmor", "BrittlebarkArmor"]

# LCurrentHP = 9
# RCurrentHP = 13

# LMaxHP = 9
# RMaxHP = 13

# #Armor tip gives +1 to base
# LArmor = 2
# RArmor = 10

# #Damage tip gives +1 to base
# LAttack = 6
# RAttack = 2

# LItems = ["SwordOfTheHero", "", ""]
# RItems = ["HornedHelmet", "HornedHelmet", "HornedHelmet"]

# LCurrentHP = 10
# RCurrentHP = 1

# LMaxHP = 10
# RMaxHP = 1

# #Armor tip gives +1 to base
# LArmor = 0
# RArmor = 1

# #Damage tip gives +1 to base
# LAttack = 3
# RAttack = 1

# #Speed tip gives +1 to base
# LSpeed = 4
# RSpeed = 0

# LGold = 0
# RGold = 0

# LLevel = 0 #Only used for basic enemies
# RLevel = 0


# Left = [LCurrentHP, LMaxHP, LAttack, LArmor, LSpeed, LItems, LLevel, LGold]
# Right = [RCurrentHP, RMaxHP, RAttack, RArmor, RSpeed, RItems, RLevel, RGold]


#Need to add basic enemies as a ez selecation stat spread with their levels
#And bosses

#Need to go through and add noneweapon trigger in all none weapon damages for sword talisman #added
#Need to add Set Item triggers #added most sets

#Might need a Powderchange tag checker if match gets added

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Whoever is faster activates all their battlestart items and then the slower one activates theirs!!!!!!!!!!!!!  #added
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#MAYBE add check if all item names are valid and make it only read the letters ie CheRry   532BomB should be valid.

#"ArmorLose" items need to set DeltaArmor = 0 inside themselves to avoid random loops giving the wrong value
#Whenever you give a new item "TakeDamage" tag it also needs "TakeDamageS" so Brittlebark Armor doesnt selftrigger
#Same with Sanguine Rose with HPRestore


#Missing a single cauldron items with honey
#Maybe I need to make a generalized gain/lose function? Made one for statuses
#Currently Stuff like BloodOrange can have its wounded effect trigger before the BattleStart but this code doesnt have this interaction.
ItemTags = {
            '':{''},
            "ArcaneBell" : {"BattleStart", "Unique", "Instrument"}, #Decrease all cooldowns by 1... Maybe just "activate" cooldown items
            "ArcaneBellS" : {"BattleStart", "Unique", "Instrument"}, 
            "BootsoftheHero" : {}, #Its just base stats
            "ChampionsArmor" : {}, #Stats
            "CherryBomb" : {"BattleStart", "Bomb", "Food"}, #Deals 1 damage two times
            "CitrineEarring" : {"EveryOtherTurn", "Jewelry", "Citrine"}, #Gain 1 Speed every other turn
            "CitrineRing" : {"BattleStart", "Jewelry", "Unique", "Ring", "Citrine"}, #Deal damage = to speed
            "ClearspringFeather" : {"BattleStart", "Water"}, #Decrease a random status effect by 1 and give it to the foe
            "ClearspringWatermelon" : {"BattleStart", "Exposed", "Wounded"}, #Decrease a random status effect by 1
            "CrackedWhetstone" : {"FirstTurn", "Stone"}, #Gain 2 attack for the first turn only
            "DeviledEgg" : {"Unique", "Sanguine"}, #Does Nothing
            "DoublePlatedArmor" : {"Exposed"}, #Gain 3 armor
            "EmeraldCrown" : {"Jewelry", "Emerald"},
            "EmeraldEarring" : {"EveryOtherTurn", "Jewelry", "Emerald"}, #Restore 1 hp
            "EmeraldRing" : {"BattleStart", "Jewelry", "Ring", "Emerald"}, #Restore 3 hp
            "EmergencyShield" : {"BattleStart"}, #Less speed than enemy, give 5 armor
            "FrostbiteGauntlet" : {"BattleStart", "Water"}, #Give the enemy 1 Freeze
            "FrostbiteTrap" : {"Wounded", "Water"}, #Give the enemy 2 freeze
            "GraniteEgg" : {"Unique", "Stone"}, #Does Nothing
            "GraniteTome" : {"Stone", "Cooldown", "Tome"}, #CD 4: Gain 6 armor
            "HolyShield" : {}, #Stats
            "HolyTome" : {"Cooldown", "Tome"}, #CD 4: Gain 3 attack
            "HornedHelmet" : {"BattleStart"}, #Gain 1 thorn
            "IceblockShield" : {"Unique", "Water", "BattleStart"}, #Self freeze 2 on battlestart
            "IronstoneBracelet" : {"Stone", "Unique", "PreFoeStrike"}, #Foe strikes deal 1 less damage if you have armor, else +1
            "KnightsArmor" : {}, #Stats
            "LeatherBelt" : {}, #Stats
            "LeatherGlove" : {}, #Its just base stats
            "LeatherVest" : {}, #Its just base stats
            "LifebloodHelmet" : {"Unique", "FirstTurn"}, #On First turn restore hp = damage from strikes Could maybe be "FirstTurnOnHit" instead??
            "LiferootGauntlet" : {"BattleStart", "Wood"}, #Gain 1 Regen
            "LiferootTome" : {"Wood", "Cooldown", "Tome"}, #CD 4: Gain 3 regen
            "LightspeedPotion" : {"BattleStart", "Unique", "Potion"}, #BatStart Restore HP = Speed
            "LightspeedElixir" : {"BattleStart", "Unique", "Potion"}, #BatStart gain max hp and Restore HP = Speed
            "LooseChange" : {}, #Gives money every night Way too complex to ask ppl for lol
            "MusclePotion" : {"Potion", "OnHit"}, #Every 3 strikes gain 1 attack
            "MuscleElixir" : {"Potion", "OnHit", "Unique"}, #Every 3 strikes gain 1 attack, 1 armor, and 1 speed
            "PetrifyingFlask" : {"Wounded", "Stone", "Potion"}, #Wounded: Gain 10 armor and 2 stun
            "PetrifyingElixir" : {"Wounded", "Stone", "Potion", "Unique"}, #Wounded: Gain 10 armor and stun everyone for 2 turns
            "PowderPlate" : {"BattleStart"}, #Give Foe 2 powder
            "PurelakeHelmet" : {"BattleStart", "Water"}, #BatStart: Gain 1 Purity
            "RedwoodCloak" : {"BattleStart", "Wood"}, #If on BatStart hp not full, restore 2
            "RedwoodHelmet": {"Exposed", "Wood"}, #Restore 3 hp on exposed
            "RedwoodRoast" : {"Wood", "Food"},
            "RoyalHorn" : {"Wounded", "Unique", "Instrument"}, #Wounded: Gain 2 gold symphony
            "RoyalHornS" : {"Wounded", "Unique", "Instrument"}, #Wounded: Gain 2 gold symphony
            "RubyCrown" : {"Jewelry", "Ruby"},
            "RubyEarring" : {"EveryOtherTurn", "Jewerly", "Ruby"}, #Deal 1 damage eot
            "RubyRing" : {"BattleStart", "Jewelry", "Ring", "Ruby"}, #Gain 2 attack and take 3 damage
            "RustyRing" : {"BattleStart", "Ring"}, #Give the foe 1 acid
            "SaffronFeather" : {"TurnStart"}, #Convert 1 speed to 2 hp even if cannot heal? ye
            "SanguineTome" : {"Unique", "Sanguine", "Cooldown", "Tome"}, #CD 6: Restore HP to full
            "SapphireCrown" : {"Jewelry", "Sapphire"},
            "SapphireEarring" : {"EveryOtherTurn","Jewelry", "Sapphire"}, #Gain 1 armor eot
            "SapphireRing" : {"BattleStart", "Jewelry", "Ring", "Sapphire"}, #Steal 2 armor from foe (if possible)
            "SerpentLyre" : {"Exposed", "Unique", "Instrument"}, #Give the foe 3 poison
            "SerpentLyreS" : {"Exposed", "Unique", "Instrument"}, #Give the foe 3 poison
            "ShieldoftheHero" : {}, #Its just base stats
            "SilverscaleFish" : {"Exposed", "Food"}, #Give the foe 1 riptide
            "SilverscaleTome" : {"Cooldown", "Tome"}, #CD 3: Give the foe 2 riptide
            "SlimeArmor" : {"BattleStart"}, #Gain 1 acid
            "SourLemon" : {"BattleStart", "Food"}, #Gain 1 acid
            "SpinyChestnut" : {"BattleStart", "Food"}, #Gain 3 thorns
            "SquiresArmor" : {}, #Stats
            "StormcloudTome" : {"Cooldown", "Tome"}, #CD 4: Stun foe 1 turn
            "SwiftstrikeBelt" : {"BattleStart"}, #Take 3 damage gain 1 strike on next turn
            "TreebarkEgg" : {"Unique", "Wood"}, #Does Nothing
            'VampireWine' : {"Wounded", "Sanguine", "Food"}, #Wounded restore 4 hp
            "VenomousFang" : {"FirstTurnOnHit"}, #First Turn: Give foe 2 poison OH
            "WeaverShield" : {"BattleStart"}, #If you have 0 base armor, gain 4 armor
            "WetEgg" : {"Water", "Unique"}, #Does Nothing
            "ArcaneGauntlet" : {"Unique"}, #All cooldowns are halved
            "ArcaneLens" : {"Unique"}, #If you have exactly 1 tome, trigger it thrice
            "ArcaneShield" : {"CooldownTrigger"}, #When a countdown effect triggers, gain 3 armor 
            "ArmorRegrowth" : {"SelfArmorLose"}, #Need a new thingy
            "BasiliskScale" : {"BattleStart"}, #BatStart: Gain 5 armor and 5 poison
            "BigBoom" : {"BattleStart", "Bomb"}, #If Foe is at or below 50%, deal 20 damage
            "BlackbriarGauntlet" : {"ArmorLose"}, #Gain 2 thorns per armor lost from foe's first strike
            "BlackbriarRose" : {"Unique", "HPRestore", "HPRestoreS"}, #Whenever you restore hp gain 2 thorns
            'BlacksmithBond' : {'Unique'},
            "BlastcapArmor" : {"Bomb", "Exposed"}, #Take 5 Damage
            'BloodChain': {'Unique'},
            #Random soooooo
            "BombBag" : {"BattleStart", "Exposed", "Wounded"}, #Spend 3 speed to retrigger a random bomb
            "BrambleBelt" : {"BattleStart"}, #Gain 2 thorns and give the foe 1 more strike
            "BrambleBuckler" : {"TurnStart"}, #Convert 1 armor to 2 thorns
            "BrambleTalisman" : {"GainThorns", "Unique"}, #Whenever you gain thorns, gain 1 armor
            #Need to add a toggle that activates on thorn lose for first time self.FirstThornLose
            "BrambleVest" : {"ThornsLose"}, #The first time you lose thorns, restore hp = to lost thorns
            "RazorvineTalisman" : {"Unique", "GainThorns"}, #When gain thorns, gain another one: ~~~~~~~~~~~~Might need to add GainThornsS
            "BrittlebarkBuckler" : {"AfterFoeFirstStrike", "Wood"}, #After Foe's First Strike take damage then lose all armor Probably can just put it as a check directly in the strike calc
            "CausticTome" : {"Cooldown", "Tome"}, #CD 3: Give the foe 3 acid, unless they have no armor, then give 3 poison
            "ChainmailCloak" : {"TurnStart"}, #If you have armor restore 2 hp
            "ClearspringCloak" : {"Exposed"}, #Remove all status effects and gain 1 armor per stack removed
            "ClearspringOpal" : {"TurnStart", "Water"}, #TS: Spend 1 speed to decrease a random status effect by 1
            "ClearspringRose" : {"HPRestore", "Unique", "Water", "HPRestoreS"}, #Whenever you restore hp, decrease a random status effect by 1.
            "Cookbook" : {"Tome"}, #This might not count idk
            "CorrodedBone" : {"BattleStart"}, #Convert 50% of Enemies hp into Armor. Rounded down?
            "CrackedBouldershield" : {"Exposed"}, #Gain 7 armor
            "CrimsonFang" : {"BattleStart", "Sanguine"}, #If your hp is full, lose 5 hp and gain 2 strikes
            #"DoubleExplosion" : {"SecondNonWeapon"}, #The 2nd time you deal nonweapon damage a turn, deal 3 damage.
            #Maybe can run the "TakeDamage" tag and then add a toggle if its the second trigger. Then reset toggle at end of turn.
            #"DoubleplatedVest" : {"SecondTakeDamage", "Unique"}, #2nd time you take damage each turn, gain 2 armor
            "EnergyDrain" : {"BattleStart", "Unique"}, # steal all foe's speed
            "ExplosivePowder" : {"BombBonus"}, #All bomb items deal 1 more damage
            "ExplosiveSurprise" : {"Explosed", "Bomb"}, #Deal 6 damage
            "FeatherweightArmor" : {"GainSpeed"}, #Gain 1 armor for every gained speed
            "FeatherweightGauntlet" : {"FirstTurn"}, #Spend 2 speed to gain 4 attack temp
            "FeatherweightGreaves" : {"TurnStart"}, #If you have 0 speed, gain 2 speed
            "FeatherweightHelmet" : {"BattleStart"}, #Spend 2 armor and gain 3 speed and 1 attack
            "FirecrackerBelt" : {"Exposed", "Bomb"}, #Deal 1 damage 3 times
            "FlameburstTome" : {"Cooldown", "Bomb", "Tome"}, #CD 4: Deal 4 and reset cooldown
            "ForgeGauntlet" : {"BattleStart"}, #Give the foe 5 armor
            "FortifiedGauntlet" : {"TurnStart"}, #If you have armor, gain an armor
            "FrostbiteArmor" : {"Water", "AfterFoeFirstStrike"}, #Enemy's first strike does 2x, then give them 4 freeze
            "FrostbiteCurse" : {"BattleStart", "Water"}, #Give yourself and foe 5 freeze each
            "GoldRing" : {"BattleStart", "Jewelry", "Ring"}, #Gain 1 gold
            "GraniteCrown" : {"BattleStart", "Stone"}, #Gain max HP = to Base armor
            "GraniteFungi" : {"TurnEnd", "Stone"}, #Gain 2 armor to you and foe
            "HeartshapedAcorn" : {"BattleStart", "Unique", "Wood"}, #If you have 0 base armor set HP to MaxHP
            "HeartshapedPotion" : {"HP1","Sanguine", "Potion", "Unique"}, #When reaching exactly 1 hp first time restore HP to MaxHP (Need to add every that loses hp)
            "HeartshapedElixir" : {"HP5","Sanguine", "Potion", "Unique"}, #When reaching below 5 hp first time restore HP to MaxHP (Need to add every that loses hp)
            #"HerosCrossguard" : {"FirstTurn", "Unique"}, #FT: On Hit trigger twice??
            "IceSpikes" : {"TurnStart", "Water"}, #If you have freeze, gain 5 thorns
            "IceTomb" : {"TurnStart", "Water"}, #If you have armor, gain 3 armor and 1 freeze.
            "ImpressivePhysique" : {"Exposed"}, #Exposed: Stun the foe for 1 turn
            "IronRose" : {"HPRestore", "Unique", "HPRestoreS"}, #Whenever you restore hp, gain 1 armor
            "IronShrapnel" : {"BattleStart", "Bomb"}, #Deal 3 damage to foe, if they have no armor deal double
            "IronstoneSandals" : {"PreStrike", "Stone"}, #Gain 3 attack when have armor
            "KindlingBomb" : {"BattleStart", "Bomb"}, #Deal 1 damage, then give the next bomb a temp damage increase.
            "LeatherBoots" : {"BattleStart"}, #More speed than foe, gain 2 attack
            "LeatherWaterskin" : {"Exposed", "Unique"}, #Gain 2 purity, repeat for each equipped water item
            "LightningBottle" : {"BattleStart", "Potion"}, #Stun yourself for 1 turn
            "LightningElixir" : {"BattleStart", "Unique", "Potion"}, #Stun yourself for 2 turns
            "MarshlightLantern" : {"Exposed"}, #Lose 3 hp and gain 8 armor
            "MoonlightCrest" : {"TurnStart", "Unique"}, #If you are below 50% hp, gain 1 regen
            "MuscleGrowth" : {"PreStrike", "Wood"}, #While you have regen, temp gain 3 attack
            "MushroomBuckler" : {"PreFoeStrike"}, #If you have poison, foe strikes do 1 less damage
            "NervePotion" : {"Potion", 'GainPoison'}, #The first time the foe gains poison, give them 1 stun
            "NerveElixir" : {"Potion", 'GainPoison', "Unique"}, #The first time the foe gains poison, give them 3 stun
            "OakHeart" : {"Unique", "Wood"}, #Effect is before battles
            "OreHeart" : {"BattleStart", "Unique", "Stone"}, #Gain 3 armor per equipped stone item
            "PiercingThorns" : {"ThornMultArmor"}, #Thorns do 2x damage to armor
            "PineconeBreastplate" : {"BattleStart", "Wood"}, #If HP = max HP at BatStart then gain PineconeBreastplateTS item
            "PineconeBreastplateTS" : {"TurnStart", "Wood"}, #Gain 1 thorn at turn start
            "PlatedGreaves" : {"Exposed"}, #Convert 3 speed to 9 armor
            "PlatedShield" : {"Unique"}, #The first time you gain armor, double it.
            "PoisonousMushroom" : {"TurnStart", "Food"}, #Gain 1 poison
            "PowderKeg" : {"Unique"}, #BatStar: If you only have 1 bomb, it triggers 3 times
            "PurelakeArmor" : {"Exposed", "Water"}, #Exposed: Remove 1 purity to gain 5 armor
            "PurelakePotion" : {"BattleStart", "Unique", "Water", "Potion"}, #Remove all armor and gain 3 purity
            "PurelakeElixir" : {"BattleStart", "Unique", "Water", "Potion"}, #Lose 5 armor and gain 5 purity
            "PurelakeTome" : {"Cooldown", "Tome"}, #CD 3: if you have purity, remove 1. Else gain 1. Reset cd
            "RiverflowTalisman" : {"GainStatus", "Unique", "Water"}, #Whenever you gain a status, gain 1 more
            "RiverflowViolin" : {"Exposed", "Unique", "Instrument", "Water"}, #Gain 4 armor Sym
            "RiverflowViolinS" : {"Exposed", "Unique", "Instrument", "Water"}, #Gain 4 armor
            "RoyalHelmet" : {"Exposed"}, #Gain 10 armor IF you have more than 20 gold
            "RustedPlate" : {"AcidDamage"}, #If the foe loses armor to acid, you gain that armor
            "SaltcrustedCrown" : {"BattleStart"}, #gain 1 riptide
            "SanguineRose" : {"HPRestore", "Unique", "Sanguine"}, #Whenever you restore 1 hp restore another (This restore doesnt count)
            "SilverAnchor" : {"LoseSpeed"}, #Whenever you lose speed, give the foe 1 riptide
            "SilverscaleArmor" : {"RiptideDamage"}, #Whenever riptide triggers, gain 2 armor
            "SilverscaleGreaves" : {"BattleStart"}, #If you have more speed, give foe 2 riptide
            "SinfulMirror" : {"Wounded", "Unique"}, #Remove all your purity
            "SlimeBomb" : {"FoeExposed", "Unique", "Bomb"}, #Remove all their acid, and deal 2 damage per acid removed
            "SlimeBooster" : {"BattleStart"}, #Convert 1 acid to 2 attack
            "SlimeHeart" : {"Wounded", "Unique"}, #Remove all acid and restore 2 hp per acid removed
            "SlimePotion" : {"Wounded", "Potion"}, #Gain armor = missing hp and gain 5 acid.
            "SlimeElixir" : {"Wounded", "Potion", "Unique"}, #Gain armor = max hp and gain 5 acid.
            "SmokeBomb" : {"BattleStart", "Bomb"}, #If less speed than foe, then gain 3 speed and give foe 3 powder
            "SpiralShell" : {"TurnStart"}, #If Stunned, give foe 1 riptide
            "SpiritualBalance" : {"BattleStart"}, #If your speed = attack. gain 3 attack
            "StillwaterPearl" : {"Unique", "RiptideTriggers"}, #Riptide can trigger twice per turn
            "StoneSteak" : {"BattleStart", "Stone", "Food"}, #If HP = MaxHP, gain 5 armor
            "StormcloudArmor" : {"BattleStart"}, #If you have more speed than armor, stun foe for 2 turns
            "StormcloudCurse" : {"BattleStart"}, #Stun yourself and the foe for 2 turns
            "SunlightCrest" : {"TurnStart"}, #If you're above 50% hp, lose 3 hp and gain 1 attack
            "SwiftstrikeCrown" : {"BattleStart", "Unique"}, #Spend 5 speed to perm gain 1 extra strike~~~~~Adds x2 when having the specifc weapon
            "TempestBreastplate" : {"Exposed"}, #Gain speed = base armor
            "ThornRing" : {"BattleStart", "Ring"}, #Take 1 damage and gain thorns equal to missing hp
            "ToxicAlgae" : {"FirstRiptide"}, #Give the foe 5 poison
            "ToxicRose" : {"HPRestore", "Unique", "HPRestoreS"}, #Whenever you restore hp, give foe 1 poison
            "TwistedRoot" : {"Exposed", "Unique", "Wood"}, #Gain 1 regen per equipped wood
            "VampiresTooth" : {"Unique"}, #If you have exactly 1 sanguine item, its healing is doubled
            "VampiricStasis" : {"Sanguine", "SkipStrike"}, #Whenever you skip your strike, restore 3 HP
            "ViperExtract" : {"Potion", "GainPoison"}, #First time foe gains poison, give them 3 more
            "ViperElixir" : {"Potion", "GainPoison", "Unique"}, #First time foe gains poison, give them 9 more
            "AcidMutation" : {"BattleStart", "PreStrike"}, #gain 1 Acid
            #"AcidMutationPS" : {"PreStrike"}, #Gain temp attack = to acid
            "AcidicWitherleaf" : {"BattleStart"}, #Give the foe acid = to your speed
            "AssaultGreaves" : {"TakeDamage", "TakeDamageS"}, #Deal 1 damage
            "BlackbriarArmor" : {"TakeDamage", "TakeDamageS"}, #Whenever you take damage, gain 2 thorns
            "BloodstoneRing" : {"BattleStart", "Sanguine", "Ring"}, #BS: Gain 5 max hp and restore 5 hp
            "BrittlebarkArmor" : {"TakeDamage", "Wood"}, #Take another damage
            "CactusCap" : {"BattleStart", "Unique"}, #Convert armor to thorns
            "ChainmailArmor" : {"Wounded"}, #RegainBaseArmor MIGHT BE IMPLIMENTED INCORRECTLY
            "CitrineGemstone" : {"Unique", "Jewelry", "Citrine"}, #Invert base speed
            "ClearspringDuck" : {"TurnStart", "Unique", "Water"}, #Gain 1 armor and decrease a random status effect by 1
            "CrimsonCloak" : {"TakeDamage", "Sanguine", "TakeDamageS"}, #Restore 1 HP
            #"DruidsCloak" : {"Unique", "HPLose", "CantHeal"}, #Whenever you lose hp, gain that much armor. Cannot restore hp
            "ElderwoodNecklace" : {"Wood"}, #Base Stats
            "EmeraldGemstone" : {"Unique", "Jewelry", "HPOverHeal", "Emerald"}, #Overhealing deals damage
            "ExplosiveArrow" : {"TurnStart", "Bomb"}, #If foe doesnt have armor, deal 2 damage
            "GrandTome" : {"Cooldown", "Unique"}, #CD 10: Retriggers all other tomes
            "Honeycomb" : {"Unique", "Food"}, 
            "IronTransfusion" : {"TurnStart"}, #Gain 2 armor lose 1 hp
            "IronskinPotion" : {"BattleStart", "Potion"}, #Gain armor = missing hp
            "IronskinElixir" : {"BattleStart", "Potion", "Unique"}, #Double your max hp. Gain armor = missing hp
            "IronstoneArmor" : {"Unique", "Stone", "PreFoeStrike"}, #Enemy strikes deal 2 less damage while you have armor
            "LifeZap" : {"BattleStart", "Unique"}, #Lose all your hp except 1 and stun the foe for 2 turns
            "LifebloodArmor" : {"BattleStart", "Sanguine"}, #Convert 50% of current hp rounded down to 2x armor
            #"LifebloodBurst" : {"Unique", "Sanguine", "Bomb"}, #Whenever you restore 3 or more hp, deal 3 damage
            "LiferootBeast" : {"TurnStart", "Unique", "Wood"}, #If you have 0 regen, gain 3 regen
            "LiferootLute" : {"Wounded", "Unique", "Instrument", "Wood"}, #Gain 3 regen
            "LiferootLuteS" : {"Wounded", "Unique", "Instrument", "Wood"}, #Gain 3 regen
            "MistArmor" : {"IgnoreSelfArmor"}, #Enemy strikes ignore armor
            "MoonlightShield" : {"TurnStart"}, #If you are below 50% hp, gain 2 armor
            "NoxiousGas" : {"TurnStart"}, #Both you and the foe get 1 poison
            "OverchargedOrb" : {"Wounded", "Unique"}, #Stun the foe for 3 turns
            "PertrifiedStatue" : {"BattleStart", "Unique", "Stone"}, #Give the foe 1 stun per stone equipped
            "PlatedHelmet" : {"TurnStart"}, #If below 50% hp, gain 2 armor
            "PurelakeChalice" : {"Water", "EveryOtherTurn"}, #Gain 1 purity eot
            "RazorBreastplate" : {"Wounded"}, #Gain thorns = foe's attack
            "RoyalShield" : {"TurnStart"}, #Convert 1 gold to 3 armor
            "RubyGemstone" : {"OnHit", "Unique", "Jewelry", "Ruby"}, #If your attack if 1, deal 4 extra damage
            "SanguineImp" : {"TurnStart", "Unique", "Sanguine"}, #Deal 1 damage and restore 1 hp
            "SanguineMorphosis" : {"TurnStart", "Sanguine"}, #Stun yourself and gain 3 regen
            "SapphireGemstone" : {"ArmorLose", "Unique", "Jewelry", "Sapphire"}, #When ever you lose armor restore than much hp
            "SerpentMask" : {"BattleStart"}, #Give the foe poison = to attack
            "SheetMusic" : {"Cooldown", "Tome", "Unique"}, #CD 6: Trigger Symphony 3 times
            "ShieldTalisman" : {"ArmorGain", "Unique"}, #Gain 1 more armor when gain armor
            "SilverscaleGauntlet" : {"Unique", "EveryOtherTurn"}, #Give 1 riptide eot
            "StonebornTurtle" : {"TurnStart", "Unique", "Stone"}, #Restore 1 hp, unless hp is full then gain 2 armor
            "StormcloudDrum" : {"Wounded", "Unique", "Instrument"}, #Give the foe 1 stun
            "StormcloudDrumS" : {"Wounded", "Unique", "Instrument"}, #Give the foe 1 stun
            "StuddedGauntlet" : {"OnHit"}, #Deal 1 damage
            "SwiftstrikeCloak" : {"BattleStart"}, #If you have more speed than foe, gain an additional strike
            "SwiftstrikeGauntlet" : {"Wounded"}, #Gain 2 additional strikes next turn
            "SwordTalisman" : {"Nonweapon", "Unique"}, #deal 1 more damage
            "TimeBomb" : {"Exposed", "Bomb"}, #Exposed deal 1 damage. This item does 2 more damage for each start turn passed.
            "TomeOfTheHero" : {"Cooldown", "Tome", "Unique"}, #CD 8: Gain 4 attack, 4 armor, and 4 speed
            "WeaverArmor" : {"BattleStart", "Unique"}, #If you have 0 base armor, gain armor = current hp
            #"ArcaneCloak" : {"Unique"}, #Reset Cooldowns after they trigger
            "BloodmoonArmor" : {"SelfDamage", "Unique"}, #If youd take damage from your own items, deal it to the foes
            #"ColdResistance" : {"Unique"}, #Freeze doubles your attack instead of halving
            #"GrandCrescendo" : {"Unique"}, #Symphony triggers all other instruments
            "GraniteThorns" : {"Unique", "Stone", "BattleStart"}, #Needs a counter to not remove thorns
            #"PrimeForm" : {"Unique"}, #Double attack while hp is full
            #"PrimordialSoup" : {"Unique"}, #Acid removes hp as well
            "RazorScales" : {"ArmorLose", "Unique"}, #If you lose armor, deal damage = to lost armor
            #"SerpentScalemail" : {"Unique", "ArmorLose"}, #Give the foe 2 poison
            #"StormtideAnchor" : {"Unique", "RiptideTriggers"}, #Stun foe 1 whenever riptide triggers
            "TwinfuseKnot" : {"BombTrigger", "Unique"}, #Bomb items trigger twice
            "BitterMelon" : {"TurnStart", "Food"}, #Convert 1 stack of another status effect to 1 poison
            "BloodOrange" : {"BattleStart", "Wounded", "Food", "Sanguine"}, #Gain 3 acid
            #"BloodOrangeW": {"Wounded", "Food", "Sanguine"}, #Convert all acid to regen
            "BloodSausage" : {"Wounded", "Food", "Sanguine"}, #Restore 1 hp 5 times
            "BloodySteak" : {"Wounded", "Saguine", "Food"}, #Restore 10 hp and 5 armor
            "BoiledHam" : {"BattleStart", "Exposed", "Wounded", "Food", "Water"}, #Decrease all status effects by 1
            "CandiedNuts" : {"BattleStart", "Food", "ThornMult"}, #Gain 3 thorns, thorns do 2x
            "CherryCocktail" : {"BattleStart", "Wounded", "Sanguine", "Bomb", "Food"}, #Deal 3 damage and restore 3 hp
            "CombustibleLemon" : {"TurnStart", "Bomb", "Food"}, #Spend 1 speed to deal 2 bomb damage
            "DeepseaWine" : {"Wounded", "Food", "RiptideTriggers"}, #Give foe 1 riptide. Whenever a riptide triggers restore 3 hp
            #"DeepseaWineR" : {"RiptideTriggers", "Food"}, #Give foe 1 riptide. Whenever a riptide triggers restore 3 hp
            "ExplosiveFish" : {"BattleStart", "Food", "Bomb"}, #Give foe 1 riptide and deal 2xfoe.riptide bombdamage
            "ExplosiveRoast" : {"BattleStart", "Bomb", "Food"}, #Deal 1 damage 4 times
            "GraniteCherry" : {"BattleStart", "Stone", "Bomb", "Food"}, #If your hp is full, gain 2 armor and deal 2 damage 3 times
            "HoneyCaviar" : {"Exposed", "Food"}, #Give foe 10 riptide
            "HoneyHam" : {"Food"}, #Doubles max hp Idk if its just base max hp
            "HoneydewMelon" : {"BattleStart", "Food"}, #Give all your status effects to the foe
            "HoneyglazedShroom" : {"TurnStart", "Food", "Unique"}, #Give the foe 2 poison
            "HornedMelon" : {"BattleStart", "Exposed", "Wounded", "Food"}, #Decrease 2 random status effects by 1 and gain that many thorns
            "LemonRoast" : {"BattleStart", "Food"}, #Gain 2 acid
            "LemonShark" : {"BattleStart", "Exposed", "Food"}, #Gain 1 acid
            #"LemonSharkE" : {"Exposed", "Food"}, #Give the foe riptide = your acid
            "LemonSyrup" : {"BattleStart", "Food"}, #Double your speed
            "LimestoneFruit" : {"BattleStart", "Stone", "Food"}, #Gain 8 armor, if hp isnt full gain 2 acid
            "MarbleMushroom" : {"BattleStart", "Stone", "Food"}, #Gain 3 poison
            "MarbledStonefish" : {"BattleStart", "Exposed", "Stone", "Food"}, #If you hp is full, gain 5 armor and give foe 1 riptide
            "MelonBomb" : {"BattleStart", "Exposed", "Wounded", "LoseStatus", "Food", "Bomb", "Water"}, #Decrease a random status effect by 1
            #"MelonBombS" : {"LoseStatus", "Food", "Bomb", "Water"}, #Whenever a status effect is decreased, deal 1 damage to foe.
            "MelonLemonade" : {"BattleStart", "Exposed", "Wounded", "Food"}, #Remove all your acid
            "MelonWine" : {"BattleStart", "Exposed", "Wounded", "Food", "Water"}, #Decrease a random status by 1 and restore 3 hp
            "MineralWater" : {"BattleStart", "Exposed", "Food", "Water"}, #If HP is full, decrease a random status by 2 and gain 5 armor
            "MoldyMeat" : {"Food"}, #Just Stats
            "MushroomSoup" : {"TurnStart", "Food", "Wood"}, #Gain 1 poison and 1 regen
            "PetrifiedChestnut" : {"BattleStart", "Food", "Stone"}, #If hp is full, gain 6 thorns and 6 armor
            "PoisonousDurian" : {"TurnStart", "Food"}, #Gain 1 poison and 1 thorns
            "PoisonousLemon" : {"BattleStart", "Food"}, #Gain 1 acid and 5 poison
            "PoisonousPufferfish" : {"BattleStart", "Food"}, #Gain 3 poison and give foe 2 riptide
            "PowderCookie" : {"BattleStart", "Food"}, #Gain 3 thorns and give foe 3 powder
            "RoastedChestnut" : {"BattleStart", "Food"}, #Gain 4 thorns
            "RockCandy" : {"BattleStart", "Stone", "Food"}, #Gain 15 armor, if hp is full gain 15 more. I think its individual
            "RockRoast" : {"Stone", "Food"}, #Just stats 
            "SharkRoast" : {"Exposed", "Food"}, #Give foe 2 riptide
            "SpikedWine" : {"Wounded", "Food"}, #Gain 5 thorns and restore 5 hp
            "SpinyKiwifruit" : {"BattleStart", "Food"}, #Gain 3 acid and gain thorns = acid
            "SpinySnapper" : {"BattleStart", "RiptideTriggers", "Food"}, #Give foe 1 riptide. Whenever riptide triggers, gain 3 thorns
            "SugarBomb" : {"TurnStart", "Bomb", "Food"}, #Deal 1 damage 3 times
            'SweetWine' : {"Wounded", "Food"}, #Wounded restore 30 hp
            "ToxicCherry" : {"TurnStart", "Food"}, #Gain 1  poison and deal 1 damage to foe
            "TrailMix" : {"BattleStart", "Food", "Bomb"}, #Deal 1 bomb damage and gain 1 thorn 3 times
            "UnderwaterWatermelon" : {"BattleStart", "Exposed", "Wounded", "Food"}, #Decrease 1 random status effect and give foe 1 riptide
        
            
            #"BloodRune" : {"Wounded", "Unique"}, #Wounded: Retriggers the last triggered wounded item.
            "EchoRune" : {"Wounded", "Unique"}, #Wounded: Retrigger a random batstart item
            #"IronRune" : {"Unique"}, #If you have 1 exposed item, it triggers thrice
            "BeltOfGluttony" : {"Unique"}, #Just Stats*
            "BootsOfSloth" : {"Unique"}, #Just Stats*
            "ChestOfLust" : {"Unique"}, #Just Stats*
            "HelmetOfEny" : {"BattleStart", "Unique"}, #Double foe's Attack


            #Need to write an effects thing for every weapon even if its just stats because that is when the strike calc should happen in the weapon effects
            #Pretty sure the bomb weapons strikes dont activate powder only the extra effects do
            # Might need some Weapons to check which tag is being searched
            "BattleAxe" : {"Weapon", "PreStrike"}, #Deal 2x if foe is armored. Maybe add "Strike" tag
            "BoomStick" : {"Weapon", "OnHit", "Bomb"}, # On hit deal one damage
            "BrittlebarkBow" : {"Weapon", "TurnStart", "Wood"}, # After 3 strikes: lose 2 attack p sure triggers once
            "ChampionsBlade" : {"Weapon"}, #Just Base Stats
            "ElderwoodStaff" : {"Weapon", "Wood"}, #Its just stats
            "FeatherweightBlade" : {"Weapon"}, #Its just stats
            "ForgeHammer" : {"Weapon", "OnHit"}, #Give the enemy 2 armor
            "FungalRapier" : {"Weapon", "BattleStart"}, #Gain 1 Poison
            "GaleStaff" : {"Weapon", "OnHit"}, #Lose 1 Speed
            "GrillingSkewer" : {"Weapon", "BattleStart", "Food"}, #Gain 1 additional strike(temp)
            "Haymaker" : {"Weapon", "TurnStart"}, # Every 3 strikes gain another one
            "HeartDrinker" : {"Weapon", "OnHit", "Sanguine"}, #On Hit: Restore 1 hp
            "HiddenDagger" : {"Weapon"}, #It gives more attack the more HD you have, aka just stats
            "IronstoneGreatsword" : {"Weapon", "Stone"}, #Just stats
            "IronstoneSpear" : {"Weapon", "PreStrike", "Stone"}, #While you have armor, temp gain 2 attack
            "KnightsBlade" : {"Weapon"}, #Just Base Stats
            "LiferootStaff" : {"Weapon", "Wounded", "Wood"}, #Gain 3 regen when wounded
            "MarbleSword" : {"Weapon", "Exposed", "Stone"}, #Exposed: Gain 3 attack
            "PacifistStaff" : {"Weapon", "Wood", "OnHit"}, #Gain 1 armor and restore 1 hp
            "RazorthornSpear" : {"Weapon", "OnHit"}, #Gain 2 thorns on hit
            "RedwoodRod" : {"Weapon", "Wood"}, #Stats
            "SilverscaleDagger" : {"Weapon", "BattleStart"}, #Give 1 Riptide
            "SlimeSword" : {"Weapon", "BattleStart"}, #Give yourself and the foe 3 acid
            "SpearshieldLance" : {"Weapon"}, #Stats
            "SquiresBlade" : {"Weapon"}, #Stats
            "StormcloudSpear" : {"Weapon", "OnHit"}, #Every 5 Strikes, stun the enemy for 2 turns. when its divisible by 5.
            "SwordOfTheHero" : {"Weapon"}, #Stats
            "WoodcuttersAxe" : {"Weapon"}, #Basically just stats like HD
            "WoodenStick" : {"Weapon", "Wood"}, #Default weapon
            "ArcaneWand" : {"Weapon", "CantAttack", "TurnStart", "Wood"}, #Cant Attack. TS: Deal 2 + Count(Tome) damage
            "BasiliskFang" : {"Weapon", "OnHit"}, #Decrease self poison by 2 and give it to foe.
            "BejeweledBlade" : {"Weapon", "Jewelry", "BattleStart"}, # Gains 2 attack per jewelry item in inv Currently not a base stats thing
            #Maybe 0 out the new temp attack for weapons right before checking if weapons have a temp increase
            "BlackbriarBlade" : {"Weapon", "PreStrike"}, #Gain 2 attack per thorn you have (Temp Increase might make other stuff that use attack stat incorrect)
            "BloodmoonDagger" : {"Weapon", "Wounded", "Sanguine"}, # Gain 5 attack and take 2 self damage
            "BloodmoonSickle" : {"Weapon", "OnHit", "Sanguine"}, # 1 Self damage
            "BubblegloopStaff" : {"Weapon", "CantAttack", "TurnStart"}, #Spend 1 speed to give the foe 1 acid and 2 poison
            #I have to fix the explosive sword, its complex now :sob:
            "ExplosiveSword" : {"Weapon", "Bomb", "BombDamage5"}, #Whenever a bomb does 5 or more explosive damage, gain 1 additional strike
            "FrostbiteDagger" : {"Weapon", "FirstTurnOnHit"}, #Give the foe freeze = your attack on hit
            "GraniteAxe" : {"Weapon", "Unique", "Stone", "OnHit"}, #Lose 3 hp and gain 3 armor
            "IcicleSpear" : {"Weapon", "Water", "Exposed"}, #Give the enemy 1 freeze for each equipped water item
            "IronstoneBow" : {"Weapon", "OnHit", "Stone"}, #On hit lose 1 speed. If Speed is 0 or less only attack every other turn (Idk if it attacks everytime the first turn you are at 0 or less speed)
            "LifebloodSpear" : {"Weapon", "FirstHPRestore"}, #Gains attack = first hp restored sounds hard
            #"LiferootHammer" : {"Weapon"}, #Regen that triggers overheal increases max hp. I assume this is before the Overheal gem
            "LightningRod" : {"Weapon", "Unique", "TurnStart"}, #If stunned, gain 1 attack
            "LightningWhip" : {"Weapon", "Unique", "TurnStart"}, #If foe is stunned, gain 1 strike
            "RingBlades" : {"Weapon", "BattleStart"}, #Steal 1 attack from foe
            "RustySword" : {"Weapon", "OnHit"}, #If the foe has no armor deal additional damage equal to foe acid
            "SanguineScepter" : {"Weapon", "Sanguine"}, #Healing doubled
            "SwiftstrikeBow" : {"Weapon"}, #Maybe add "StrikeGain" whenever you gain a strike, gain another one
            "SwiftstrikeRapier" : {"Weapon", "BattleStart"}, #If you have more speed than foe, gain 2 strikes
            "WaveBreaker" : {"Weapon", "CantAttack", "BattleStart"}, #Give the foe 2*(negative base attack) riptide
            "BloodlordsAxe" : {"Weapon", "BattleStart", "Sanguine"}, #Foe loses 5 hp, you restore 5 hp
            "BrittlebarkClub" : {"Weapon", "Wood", "Exposed", "Wounded"}, #Exp or Wound lose 2 attack
            "ChainmailSword" : {"Weapon", "Exposed"}, #Gain armor equal to base armor
            "FrozenIceblade" : {"Weapon", "BattleStart", "Water"}, #Gain 3 freeze
            "GemstoneScepter" : {"Weapon", "Jewelry", "OnHit"}, #Gain an on hit effect if you have emerald(+1HP), ruby(+1damage), sapphire(+1Armor), or citrine(+1spd) items
            "GraniteHammer" : {"Weapon", "Stone", "OnHit"}, #Convert 1 armor to 2 attack p sure this the right order to gain the attack
            "GraniteLance" : {"Weapon", "Stone"}, #Stat effect 2x base armor
            "GrindstoneClub" : {"Weapon", "Stone"}, #Effect +2 attack to next weapon equipped (Makes figuring out weapon base stats more annoying)
            "KingsBlade" : {"BattleStart"}, #Wounded and Exposed trigger at battle start
            "LeatherWhip" : {"BattleStart"}, #Gain 5 max hp
            "LifestealScythe" : {"Weapon", "OnHit", "Sanguine"}, #Restore HP = Damage done to HP
            "MeltingIceblade" : {"OnHit", "Water"}, #Lose 1 attack
            "MoonlightCleaver" : {"PreventStatusGain"}, #If below 50% hp cannot gain status
            "PurelakeStaff" : {"BattleStart", "Water"}, #BS: Gain 2 purity. OH: Lose 1 purity
            "PurelakeStaffOH" : {"OnHit", "Water"}, #BS: Gain 2 purity. OH: Lose 1 purity
            "QuickgrowthSpear" : {"Weapon", "EveryOtherTurn", "Wood"}, #Gain 1 attack and restore 1 HP
            "RiverflowRapier" : {"Water", "FirstGainStatus"}, #First time you gain a new status effect, gain 1 strike
            "RoyalCrownblade" : {"Weapon", "OnHit"}, #Gain 1 Gold
            "RoyalScepter" : {"Weapon", "PreStrikeL", "Jewelry"}, #Set temp attack equal to gold. Cannot have more than 10 gold
            "SerpentDagger" : {"Weapon", "OnHit"}, #Every 3 strikes give the foe 4 poison
            "SilverscaleTrident" : {"Weapon", "OnHit"}, #Give 1 riptide
            "StoneslabSword" : {"Weapon", "OnHit", "Stone"}, #Gain 2 armor
            "ThunderboundSabre" : {"Weapon", "BattleStart"}, #Stun yourself for 2 turns
            "TwinBlade" : {"Weapon", "BattleStart"}, #Base strikes count = 2 #Might want to make a PreBattle Tag??
            #"AncientWarhammer" : {"Weapon", "OnHit"}, #OH: Remove all of the foe's armor
            "BearclawBlade" : {"Weapon", "PreStrikeL"}, #Attack = Missing HP
            #"DashmastersDagger" : {"Weapon", "BattlseStart"}, #Gain additional strikes equal to speed
            #"LakebedSword" : {"Weapon"}, #Doubles the effects from Purity
            "MountainCleaver" : {"Weapon", "BattleStart", "Stone"}, #Attack = Base Armor
            "SpikyClub" : {"Weapon"},  #Maybe GainThorns tag? or add it to everything that adds thorns. GainThorns becomes GainAttack
            "TempestBlade" : {"Weapon", "PreStrikeL"}, #Attack = Speed
            #"CleaverOfWrath" : {"Weapon"}, #Your max hp is always 1 (Disables all max hp changes)
            #"ScepterOfGreed" : {"Weapon"}, #Cant gain gold. (Disables all gold gain)
            "SwordOfPride" : {"Weapon", "BattleStart"}, #If the foe has more attack, armor, or speed, take 3 damage
            #"BeeStinger" : {"Weapon", "FirstTurn", "Food"}, #Give the foe 4 poison, 3 acid, and 2 stun on hit
            "BlackbriarBow" : {"Weapon", "CantAttack", "TurnStart"}, #Turn Start gain thorns = to your attack
            #"BrokenWineglass" : {"Weapon", "Wounded"}, #When wounded, on your next turn keep striking until the foe is wounded
            "CherryBlade" : {"Weapon", "BattleStart", "Exposed", "Food", "Bomb"}, #Deal 4 damage on batstart and exposed
            "DeathcapBow" : {"Weapon", "BattleStart", "TurnStart"}, #BS: Gain 3 Poison. TS: Gain 1 additional strike, if you are poisoned
            #"DeathcapBowTS" : {"Weapon", "TurnStart"}, #Gain 1 additional strike, if you are poisoned
            "HamBat" : {"Weapon", "BattleStart", "Food", "Wood"}, #Gain 2 additional strikes
            "LemontreeBranch" : {"Weapon", "OnHit", "Food", "Wood"}, #Spend 2 speed to gain an additional strike
            "MelonvineWhip" : {"Weapon", "OnHit", "Food", "Water"}, #On hit remove 1 stack of a random status effect on self
            "RocksaltSword" : {"Weapon", "TurnStart"}, #if your hp is full, gain 1 additional strike
            "SilverscaleSwordfish" : {"Weapon", "BattleStart", "FirstTurn", "Food"}, #Gain 1 extra strike on battle start, #First Turn on hit give the foe 1 riptide
            #"SilverscaleSwordfishFT" : {"Weapon", "FirstTurn", "Food"}, #First Turn on hit give the foe 1 riptide

            #Blade Edges (Blacksmith)
            "AgileEdge" : {"Edge", "FirstTurn"}, #Gain 1 additional strike on first turn
            "BleedingEdge" : {"Edge", "OnHit"}, #Restore 1 HP
            "BluntEdge" : {"Edge", "OnHit"}, #Gain 1 armor
            "CleansingEdge" : {"Edge", "PreventStatusGain"}, #Ignore the first Status effect you are afflicted with
            "CuttingEdge" : {"Edge", "OnHit"}, #Deal 1 Damage
            "FeatherweightEdge" : {"Edge", "OnHit"}, #Convert 1 Speed to 1 Attack
            "FreezingEdge" : {"Edge", "BattleStart"}, #Give foe 3 freeze
            "GildedEdge" : {"Edge", "OnHit"}, #If Gold < 10, Gain 1 gold
            "JaggedEdge" : {"Edge", "OnHit"}, #Gain 2 thorns and take 1 self damage
            "OakenEdge" : {"Edge", "BattleStart"}, #Gain 3 regen
            "OozingEdge" : {"Edge", "OnHit"}, #If foe poison = 0, give 2 poison
            "PetrifiedEdge" : {"Edge", "OnHit"}, #Double your attack, OH: gain 1 stun
            "PlatedEdge" : {"Edge", "OnHit"}, #Convert 1 speed to 3 armor
            "RazorEdge" : {"Edge", "BattleStart"}, #Gain 1 attack
            "SmokingEdge" : {"Edge", "OnHit"}, #Give 1 powder to foe
            "StormcloudEdge" : {"Edge", "BattleStart"}, #Stun foe for 1 turn
            "WhirlpoolEdge" : {"Edge", "OnHit"}, #Every 3 strikes, give 1 riptide

            #Item Sets
            "BloodmoonStrike" : {"Set", "Wounded"}, #On your next turn restore hp = to damage done by strikes
            "BriarGreaves" : {"Set", "TakeDamage", "TakeDamageS"}, #On take damage, gain 1 thorn
            "BrittlebarkBlessing" : {"Set"}, #Makes it so brittlebark stuff doesnt have a downside
            "ElderwoodMask" : {"Set", "BattleStart"}, #Double all base attack, armor, speed
            "HerosReturn" : {"Set"}, #Base Stats
            "Highborn" : {"Set"}, #Retrigger all rings
            "IronbarkShield" : {"Set"}, #If Hp is full, gain 1 armor at turn start
            "IronbarkShieldTS": {"Set"}, #1 Armor Gain at turn start 
            "LifebloodTransfusion" : {"Set", "BattleEnd"}, #Restore 10 HP after battle. Kinda just not useful to include?
            "RawHide" : {"Set", "EveryOtherTurn"}, #Gain 1 attack
            "RedwoodCrown" : {"Set", "Wounded"}, #Restore HP to Full
            "SaffronTalon" :{"Set", "OnHit"}, #Gain 1 speed on hit
            "SteelplatedThorns" : {"Set", "ThornsLose"}, #Whenever you lose thorns gain that much armor
            "BasilisksGaze" : {"Set", "BattleStart"}, #Your foe is stunned for 2 turns
            "ChampionsGreaves" : {"Set"}, #Just Stats
            "DeadlyToxin" : {"Set", "GainPoison"}, #First time foe gains poison, give 2 acid
            "GraniteQuill" : {"Set"}, #Makes Regen give armor instead of hp
            "HolyCrucifix" : {"Set"}, #Just changes base stats
            "IronstoneCrest" : {"Set", "TurnStart"}, #Steal 2 armor from foe
            "IronstoneFang" : {"Set", "FirstTurnOnHit"}, #Gain 3 armor on hit
            "MarbleAnvil" : {"Set", "BattleStart"}, #
            "MarshlightAria" : {"Set", "Exposed"}, #When exposed: Trigger symphony twice
            "SeafoodHotpot" : {"Set", "BattleStart"}, #Gain 2 armor per speed
            #Gotta redo the vamp cloak to check for stun at turn start *maybe*
            "VampireCloak" : {"Set"}, #TS: If you are stunned, double all healing this turn
            "WeaverMedallion" : {"Set", "TurnStart"}, #Spend 1 armor to gain 1 attack
            "IronChain" : {"Set"}, #Double your base armor
            "IronstoneArrowhead" : {"Set", "OnHit"}, #Gain 1 armor on hit
            "IronstoneOre" : {"Set", "BattleStart"}, #Gain armor = negative speed
            "SanguineGemstone" : {"Set", "OnHit"}, #If your attack == 1, restore 1 hp on hit? Idk if its sanguine

            #Blessings might have in battle effects? Idk yet

            #Enemies 
            "Bat" : {"OddEveryOtherTurn"},#Heal 1+Lvl HP OnHit every other strike not on the first strike
            "Bear" : {"PreStrike"},#Gains 3+Lvl attack if foe has armor
            #"Beaver" : {"BattleStart"}, #Gains 3+Lvl regen?
            #"Frog" : {"Exposed"}, #Gain 1 +Lvl armor on exposed?
            "Hedgehog" : {"BattleStart"},#Gains 3+Lvl thorns on BattleStart
            #"HoneyBee" : {"FirtTurn"}, #Give the foe 4 poison, 3 acid, and 2 stun on hit? With some scaling
            #"Mosquito" : {"BattleStart"}, #Gain attack = Speed - player speed >= 0
            #"Raccoon" : {"SuperBattleStart"}, #Steals 1 + lvl items at random
            "Raven" : {"OnHit"}, # OnHit steals 1+Lvl gold
            #"Snake" : {"FirstTurn"}, #Gives 2 + Lvl? poison on first turn hit
            "Spider" : {"BattleStart"}, #If Spider is faster, then it deals 3+Lvl damage BattleStart
            #"Turtle": {"TakeDamage"}, #lose all armor
            "Wolf" : {"PreStrike"}, #If Foe.CurrenHP <=5 temp attack is set to +2+Lvl




        

            #Night 1 Bosses
            "BlackKnight" : {"BattleStart"}, # Gain attack = Foe.Attack + 2 Might be prebattle but p sure its a battlestart speed, might be slower tho
            "BloodmoonWerewolf" : {"PreStrike"}, #When player is below 50% HP, gains 5 attack
            "BrittlebarkBeast" : {"TakeDamage"}, #Whenever it takes damage take 3 more
            "IronstoneGolem" : {"Exposed"}, #When exposed lose 3 attack
            "RazorclawGrizzly" : {"IgnoreFoeArmor"}, #Attacks ignore armor
            "RazortuskHog" : {"FirstTurn"},#If Razortusk Hog has more speed, first strike does 10 extra damage
            #Swamp Night 1
            #"CarnivorousSlime" : {"BattleStart"}, #Gives 3 acid and converts all player's hp except 1 into armor
            #"FungalGiant" : {"BattleStart"}, #Gains 1 poison for each status effect the player has
            #"IronshellSnail" : {"BattleStart"}, #Gains 5 acid
            #"StormcloudDruid" : {"OnHit"}, #Stun the player for 1 turn every other strike
            #"SwampsongSiren" : {"BattleStart"}, #Gives the Player -2 attack
            #"ToxicMiretoad" : {"BattleStart"}, #Steals all the player's armor and gives 3 poison
            #Night 2 Bosses
            "BlackbriarKing" : {}, #CANNOT ATTACK, instead gains 2 thorns every turn. 4 if wounded(Below 50% hp)
            #"FrostbiteDruid" : {"OnHit"}, #Gives the player 1 freeze
            #"GoldwingMonarch" : {"Wounded"}, #Steals all the players gold and heals for 2*Gold
            "MountainTroll" : {""}, #Only strikes every other turn
            #"RedwoodTreant" : {"PreStrike"}, #Temp gains 3 attack if player has no armor
            "SwiftstrikeStag" : {"BattleStart"}, #Strikes 3 times
            #Swamp Night 2
            #"ClearspringSpirit" : {"BattleStart", "OnHit"}, #Gains 10 Purity. On Hit randomly decrease a self or player status
            #"GraniteGriffin" : {"Wounded"}, #Gains 40 armor and 4 stun
            #"LiferootExperiment" : {"BattleStart"}, #Gains 10 regen
            #"RockshellTortoise" : {""}, #Whenever it is struck, gains 4 armor
            #"SilverscaleShark" : {"TurnStart"}, #Gives the player 2 riptide. Gains 1 temp attack per player riptide
            #"StonescaleBasilisk" : {"OnHit"}, #Gives 2 poison on hit
            #Night 3 boss
            "Leshen" : {""}, #Currently does nothing
            "WoodlandAbomination" : {"TurnStart"}, #Gain an attack
            #Swamp Night 3
            #"SwamplandHydra" #Is a hecking mess, basically 4 different bosses as one enemy
            #MiniBosses
            "IronshellBeetle" : {"OnHit"}, #Lose 1 attack on hit (Up to 0)
            #"LifebloodCount" : {"OnHit"}, #Restores 3 hp
            "SilkweaverQueen" : {"TurnStart"}, #Turn Start steals 1 speed. If the foe has 0 or less speed, deal 3 damage instead
            #Swamp MiniBosses
            #"CovenPlaguemother" : {"OnHit"}, #Gives the player 2 stacks of a random status they dont have
            #"MurkwaterGator" : {"BattleStart"}, #Gives the player riptide = to player's attack
            #"PalaceSentinel" : {"TurnStart"}, #If it is slower, self stun and gain 2 speed
            }


# ["CurrentHP", "MaxHP", "Attack", "Armor", "Speed", "SpecialEffect", "Level", "Gold"] Special effect can just be an item

#100% Missing a lot of stats
def Enemies(Name, Level):
    #Assuming level = 0 on night 1
    Lvl = Level - 1
    if Name == "Bat":
        #Correct
        Stats = [4+2*Lvl, 4+2*Lvl, 1+Lvl, 0, 2+Lvl, ["Bat"], Level, 0] #Heal 1+Lvl HP OnHit every other strike

    if Name == "Bear":
        #Correct
        Stats = [3+2*Lvl, 3+2*Lvl, 1+Lvl, 2+Lvl, 0+Lvl, ["Bear"], Level, 0] #Gains 3+Lvl attack if foe has armor

    if Name == "CrazedHoneybear":
        #14, 6, 8, 4 LVL 3 +5 damage to armored foes
        Stats = [] #10, 4, 6, 2 LVL 2 +4 damage to armored foes

    if Name == "Hedgehog":
        #Armor is 1 to 2 to 4?
        Stats = [1+Lvl, 1+Lvl, 1, max(1, 2*Lvl), 0, ["Hedgehog"], Level, 0] #Gains 3+Lvl thorns on BattleStart

    if Name == "Raven": #Might be able to make it be one check enemy and then the level scales the stats?
        #Correct
        Stats = [3+2*Lvl, 3+2*Lvl, 0, 0, 2+Lvl, ["Raven"], Level, 0] #OnHit steals 1+Lvl gold


    if Name == "Spider": #Might be able to make it be one check enemy and then the level scales the stats?
        #Correct
        Stats = [2+Lvl, 2+Lvl, 1, 0, 2+Lvl, ["Spider"], Level, 0] #If Spider is faster, then it deals 3+Lvl damage BattleStart


    if Name == "Wolf": #Might be able to make it be one check wolf and then the level scales the stats?
        #Attack maxes to 2 at lvl 3
        Stats = [3+3*Lvl, 3+3*Lvl, 1+min(1, Lvl), 0, 1+Lvl, ["Wolf"], Level, 0] #If Foe.CurrenHP <=5 temp attack is set to +2+Lvl

    #Bosses-Night 1
    if Name == "BlackKnight":
        Stats = [10, 10, 0, 5, 0, ["BlackKnight"], Level, 0] #Gain attack = Foe.Attack + 2

    if Name == "BloodmoonWerewolf":
        Stats = [15, 15, 3, 0, 1, ["BloodmoonWerewolf"], Level, 0] #When player is below 50% HP, gains 5 attack

    if Name == "BrittlebarkBeast":
        Stats = [40, 40, 3, 0, 2, ["BrittlebarkBeast"], Level, 0] #Whenever you take damage take 3 more

    if Name == "IronstoneGolem":
        Stats = [5, 5, 4, 15, 1, ["IronstoneGolem"], Level, 0] #When exposed lose 3 attack

    if Name == "RazorclawGrizzly":
        Stats = [10, 10, 3, 5, 2, ["RazorclawGrizzly"], Level, 0] #Attacks ignore armor

    if Name == "RazortuskHog":
        Stats = [5, 5, 4, 0, 4, ["RazortuskHog"], Level, 0] #If Razortusk Hog has more speed, first strike does 10 extra damage

    #Bosses-Night 2
    if Name == "BlackbriarKing":
        Stats = [50, 50, 0, 0, 0, ["BlackbriarKing"], Level, 0] #CANNOT ATTACK, instead gains 2 thorns every turn. 4 if wounded(Below 50% hp)

    if Name == "MountainTroll": #Currently lazy coding only works if Troll stays 0 speed
        Stats = [20, 20, 10, 10, 0, ["MountainTroll"], Level, 0] #Attack every other turn

    if Name == "SwiftstrikeStag":
        Stats = [10, 10, 3, 5, 5, ["SwiftstrikeStag"], Level, 0] #3 Strikes per turn

    #Bosses-Night 3
    if Name == "Leshen":
        Stats = [50, 50, 7, 0, 3, ["Leshen"], Level, 0] #Nothing?

    if Name == "WoodlandAbomination": #Phase 2, but you heal to full hp sooooo, its just a new fight
        Stats = [100, 100, 0, 50, 2, ["WoodlandAbomination"], Level, 0] #Gains an attack at start of turn
    
    #Minibosses
    if Name == "IronshellBeetle":
        Stats = [10, 10, 7, 50, 0, ["IronshellBeetle"], Level, 0] #OnHit lose 1 attack

    if Name == "SilkweaverQueen":
        Stats = [20, 20, 3, 10, 4, ["SilkweaverQueen"], Level, 0] #Turn Start steals 1 speed. If the foe has 0 or less speed, deal 3 damage instead

    #Vampire guy, Heals 3 on hit

    return Stats

#need to add equipments (Including enemy and bosses effects as equipment) and blacksmith effects
class Player:
    def __init__(self, Stats, Order): #self, CurrentHP, MaxHP, Attack, Armor, Speed, Items, Lvl, Gold, Order):
        
        self.CurrentHP = Stats[0]
        self.MaxHP = Stats[1]
        self.Attack = Stats[2]
        self.Armor = Stats[3]
        self.Speed = Stats[4]
        self.Items = Stats[5]
        self.Level = Stats[6]
        self.Gold = Stats[7]
        self.Order = Order

        self.WoundTriggers = 0
        #Determines if you start above wounded threashhold
        if self.CurrentHP/self.MaxHP > 0.5: 
            self.WoundTriggers = 1

        self.ExposedTriggers = 1
        if "BlacksmithBond" in self.Items:
            self.ExposedTriggers = 2

        self.GainedArmor = False
        if self.Armor > 0:
            self.GainedArmor = True

        self.BaseArmor = np.copy(self.Armor)
        self.DeltaSpeed = 0
        self.Powder = 0
        self.BombMult = 1
        self.TempBombBonus = 0
        self.BombBonus = 0
        self.Thorns = 0
        self.ThornsDecrease = 0
        self.FirstThornLose = True
        self.StrikesCount = 1 #Twin Blades should set this to 2 also Ig?
        self.BaseStrikesCount = 1 #Twin Blades should set this to 2
        self.FirstStrike = True

        # self.ArmorShielding = 0
        # if "IronstoneBracelet" in self.Items:
        #     self.ArmorShielding = 1

        self.FirstFoeStrikeMult = 1
        if "FrostbiteArmor" in self.Items:
            self.FirstFoeStrikeMult = 2

        self.DeltaArmor = 0 #Purely used for armor lose currently then run a check for armorlose items then reset deltaarmor to 0
        self.FirstTurn = True
        self.TempAttack = 0
        self.ThornsTriggers = 0
        self.StrikeMult = 1
        if "PetrifiedEdge" in self.Items:
            self.StrikeMult = 2

        self.StrikeCounter = 0 #Only Used for Weapons
        self.TurnCounter = 0
        self.Cooldown = 0 #need to increment every turn and from other items
        self.CooldownReduction = 0 #Decreases max CD
        self.CooldownMult = 1 #Multiplicative Reduction of CD
        if "ArcaneGauntlet" in self.Items:
            self.CooldownMult = 0.5
            
        self.TomeTriggers = 1
        if "ArcaneLens" in self.Items:
            self.TomeTriggers = 3
            
        self.GraniteTome = True
        self.HolyTome = True
        self.LiferootTome = True
        self.SanguineTome = True
        self.SilverscaleTome = True
        self.StormcloudTome = True
        self.CausticTome = True
        self.GrandTome = True
        self.SheetMusic = True
        self.TomeOfTheHero = True
        self.GrandTomeRetriggers = False

        self.Odd = True #Used exclusively for IronstoneBow
        self.DamageFromFoeStrike = 0
        self.HPloseFromFoeStrike = 0
        self.FirstHealToggle = True #Purely to count if you have healed once to fine the first heal amount for the one lifebloodspear
        self.Freeze = 0
        self.Poison = 0
        self.Riptide = 0
        self.FirstRiptide = True
        self.Acid = 0
        self.Stun = 0
        self.Purity = 0
        self.Regen = 0
        self.FirstThornLose = True

        self.SanguineMult = 1
        if "VampiresTooth" in self.Items:
            self.SanguineMult = 2

        self.SanguineScepterMult = 1
        if "SanguineScepter" in self.Items:
            self.SanguineScepterMult = 2

        self.TwilightCrestMult = 1
        if "TwilightCrest" in self.Items:
            self.TwilightCrestMult = 2
        
        self.VampireCloak = 1
        if "VampireCloak" in self.Items:
            self.VampireCloak = 2

        self.BombTrigger = 1
        if "TwinfuseKnot" in self.Items:
            self.BombTrigger = 2
        if "PowderKeg" in self.Items and Count(self, "Bomb") == 1:
            self.BombTrigger = 3

        self.RingTrigger = 1
        if "Highborn" in self.Items: #Retrigger all rings
            self.RingTrigger = 2

        self.NoBBB = True
        if "BrittlebarkBlessing" in self.Items:
            self.NoBBB = False

        self.HP1PotionTrigger = True
        self.HP1ElixirTrigger = True
        self.NervePot = True
        self.NerveElixir = True
        self.ViperPot = True
        self.ViperElixir= True
        self.DeadlyToxin = True

        self.PlatedShield = False
        if "PlatedShield" in self.Items:
            self.PlatedShield = True
        
        self.StatusesGained = []
        self.PreventStatusGain = False
        self.FirstStatus = True
        self.FreezeMult = 1
        #self.RHeal = 0 Prob not using

    #That is search weapons (Blacksmithing is added after the base effects) then items.
    #Hit damage, on hit, blacksmith edge, foes reaction to being hit (thorns from foe, brittlebark armor etc.)
    #Player.Items = ["Weapon", "Edge", "Inv"]
    def Strike(self, Foe):
        self.FreezeMult = 1
        if self.Freeze > 0:
            self.FreezeMult = 0.5
        SC = np.copy(self.StrikesCount)
        # if Foe.Armor > 0:
        #     mult = 1
        # elif Foe.Armor == 0:
        #     mult = -1
        # else:
        #     print("Warning Armor somehow became negative")
        #If you have Ironstone bow
        if "IronstoneBow" in self.Items or "MountainTroll" in self.Items:
            if self.Speed > 0 and ("IronstoneBow" in self.Items):
                self.StrikeLoop(Foe, SC)
                self.CheckThornsLose(Foe)

            elif self.Speed <= 0 and self.Odd: #And speed <=0, attack every other turn, might not work right if you gain 2 speed everyother turn or smth
                self.Odd = False
                self.StrikeLoop(Foe, SC)
                self.CheckThornsLose(Foe)
            else:
                self.Odd = True #When speed <= 0 and its not odd cannot attack

        elif Count(self, "IgnoreFoeArmor") > 0 or Count(Foe, "IgnoreSelfArmor") > 0: #{"IgnoreArmor"}, #Attacks ignore armor"
            for i in range(0, SC): #Check if death occurs before each strike/after?
                self.TempAttack = 0
                self.StrikeCounter = self.StrikeCounter + 1
                PreStrikeAttackBonus(self, Foe)
                PreStrikeL(self, Foe) #Need to set self.TempAttack = 0 since these weapons set attack not gain?
                self.StrikeCalcIgnoreArmor(Foe) #Might need to add multistrikes here
                if np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)*Foe.FirstFoeStrikeMult > 0:   #Might need to go in the above for loop????
                    TakeDamage(Foe, self) #TakeDamage check for items
                self.StrikeMult = 1
                self.ThornsDamage(Foe) #Adds thorns activation
                Foe.FirstFoeStrikeMult = 1
            self.StrikesCount = self.BaseStrikesCount
            self.CheckThornsLose(Foe)

        else:
            self.StrikeLoop(Foe, SC)
            self.CheckThornsLose(Foe)
        return Foe

    def StrikeLoop(self, Foe, SC):
        self.FreezeMult = 1
        if self.Freeze > 0:
            self.FreezeMult = 0.5
        for i in range(0, SC): #Check if death occurs before each strike/after?
            self.TempAttack = 0
            self.StrikeCounter = self.StrikeCounter + 1
            PreStrikeAttackBonus(self, Foe)
            PreStrikeL(self, Foe) #Need to set self.TempAttack = 0 since these weapons set attack not gain?
            self.StrikeCalc(Foe) #Might need to add multistrikes here
            if np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)*Foe.FirstFoeStrikeMult > 0:   #Might need to go in the above for loop????
                TakeDamage(Foe, self) #TakeDamage check for items
            self.StrikeMult = 1
            if self.FirstStrike:
                Foe.Search("AfterFoeFirstStrike", self) #Unsure what Phase this is. 
                self.FirstStrike = False
            self.ThornsDamage(Foe) #Adds thorns activation
            Foe.FirstFoeStrikeMult = 1
        self.StrikesCount = self.BaseStrikesCount
        

    def StrikeCalc(self, Foe):
        self.FreezeMult = 1
        if self.Freeze > 0:
            self.FreezeMult = 0.5
        StrikeMult(self, Foe)
        if np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)*Foe.FirstFoeStrikeMult > 0:
            Foe.DamageFromFoeStrike = np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)
            Foe.HPloseFromFoeStrike = max(0, np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)- Foe.Armor)

            Foe.CurrentHP = min(Foe.CurrentHP, Foe.CurrentHP + Foe.Armor - np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult))
            HP1Check(Foe, self)
            Foe.DeltaArmor = min(Foe.Armor, np.floor((self.StrikeMult*(self.Attack + self.TempAttack))))
            ArmorLose(Foe, self)
            Foe.DeltaArmor = 0
            Foe.Armor = max(0, Foe.Armor - np.floor((self.StrikeMult*(self.Attack + self.TempAttack))))

        #Might need to go into the strike function in its own seperate for loop??????????
        OnHit(self, Foe) #Checks for On hit effects including weapons and blacksmithed and include dealdamage
    
    def StrikeCalcIgnoreArmor(self, Foe):
        self.FreezeMult = 1
        if self.Freeze > 0:
            self.FreezeMult = 0.5
        StrikeMult(self, Foe)
        if np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)*Foe.FirstFoeStrikeMult > 0:
            Foe.DamageFromFoeStrike = np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)
            Foe.HPloseFromFoeStrike = max(0, np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult)) #Idk why its -Foe.Armor here?
            Foe.CurrentHP = min(Foe.CurrentHP, Foe.CurrentHP + Foe.Armor - np.floor((self.StrikeMult*(self.Attack + self.TempAttack))*self.FreezeMult))
            HP1Check(Foe, self)
        #Might need to go into the strike function in its own seperate for loop??????????
        OnHit(self, Foe) #Checks for On hit effects including weapons and blacksmithed and include dealdamage
    

    def ThornsDamage(self, Foe):
        if Foe.Thorns > 0:
            c = Foe.Count("ThornMult")
            ThornsMult = 2**c
            if self.Armor > 0:
                c = Foe.Count("ThornMultArmor")
                ThornsMult = ThornsMult * 2**c
            #basically this only checks for it once?
            # if "CandiedNuts" in Foe.Items:
            #     ThornsMult = 2*ThornsMult
            # elif "PiercingThorns" in Foe.Items:
            #     if self.Armor > 0:
            #         ThornsMult = 2*ThornsMult
            DealDamage(ThornsMult*Foe.Thorns, Foe, self)

    def CheckThornsLose(self, Foe):
        if Foe.ThornsTriggers > 0:
            Foe.ThornsTriggers = Foe.ThornsTriggers - 1
        else:
            StatusInterp("Thorns", Foe, self, -Foe.Thorns)
            #ThornsLose(Foe, self, Foe.Thorns)
            #Foe.Thorns = 0
    
    def Wounded(self, Foe):
        if self.CurrentHP/self.MaxHP <= 0.5 and self.CurrentHP>0 and self.WoundTriggers > 0:
            P = self
            P.WoundTriggers = self.WoundTriggers - 1
            #Check each players inv slot by slot for wounded in self and wounded in foe if foe has blood chain
            if "BloodChain" in Foe.Items:
                P.MultiSearch("Wounded", Foe, "Wounded") #It might activate all the faster persons items first instead of a slot by slot check
            else:
                P.Search("Wounded", Foe)

    def Exposed(self, Foe):
        P = self
        if self.Armor == 0 and self.ExposedTriggers > 0 and self.GainedArmor == True:
            P.ExposedTriggers = self.ExposedTriggers - 1
            P.GainedArmor = False #Toggles checkGainedArmor
            self.MultiSearch("Exposed", Foe, "FoeExposed")
            # self.Search("Exposed", Foe)  #Add all exposed triggers here
            # Foe.Search("FoeExposed", self)

    def Count(self, Tag):
        P = self
        x = 0
        for slot in range(0, len(P.Items)):
            if Tag in ItemTags[P.Items[slot]]:
                x = x + 1
        return x

    def Search(self, Tag, Foe):
        P = self
        for slot in range(0, len(P.Items)): #max(len(P.Items), len(Foe.Items))):
            if Tag in ItemTags[P.Items[slot]]:
                [P, Foe] = ItemsEffect(Tag, self.Items[slot], P, Foe)

    def RandomSearch(self, Tag, Foe):
        P = self
        List = []
        for slot in range(0, len(P.Items)): #max(len(P.Items), len(Foe.Items))):
            if Tag in ItemTags[P.Items[slot]]:
                List = List.append(slot)
        #This *probably* works Idk
        if List != []:
            RanNumber = random.randint(0, len(List))
            slot = int(List(RanNumber))
            [P, Foe] = ItemsEffect(Tag, self.Items[slot], P, Foe)

    def MultiSearch(self, TagP, Foe, TagF): #Seperate multisearch REQUIRES Speed order check (Outside when used)??
        P = self
        if self.Order == "First":
            for slot in range(0, max(len(P.Items), len(Foe.Items))):
                if TagP in ItemTags[P.Items[slot]]:
                    [P, Foe] = ItemsEffect(TagP, self.Items[slot], P, Foe)

                if TagF in ItemTags[Foe.Items[slot]]:
                    [Foe, P] = ItemsEffect(TagF, Foe.Items[slot], Foe, P)

        if self.Order == "Second":
            for slot in range(0, max(len(P.Items), len(Foe.Items))):
                if TagF in ItemTags[Foe.Items[slot]]:
                    [Foe, P] = ItemsEffect(TagF, Foe.Items[slot], Foe, P)
                if TagP in ItemTags[P.Items[slot]]:
                    [P, Foe] = ItemsEffect(TagP, self.Items[slot], P, Foe)

    def RandomStatus(self, Foe, Value): #Look at Player/ Foe? / Both? (Might add more functionality) and selects a status effect they currently have.
        # StatusFunctions = {
        #     "Thorns": GainThorns,
        #     "Freeze": Freeze,
        #     "Regen": GainRegen,
        #     "Poison": GainPoison,
        #     "Stun": Stun,
        #     "Riptide": GainRiptide,
        #     "Acid": GainAcid,
        #     "Purity": GainPurity,
        # }
        Statuses = ["Thorns", "Freeze", "Regen", "Poison", "Stun", "Riptide", "Acid", "Purity"] #list(StatusFunctions.keys())
        CurrentStatus = []
        StatusStacks = 0
        PickedStatus = "null"
        #key: use getattr and setattr
        for ii in range(0, len(Statuses)):
            if getattr(self, Statuses[ii]) > 0:
                CurrentStatus.append(Statuses[ii])
        if CurrentStatus != []:
            PickedStatus = random.choice(CurrentStatus)
            StatusStacks = getattr(self, PickedStatus)
            StatusInterp(PickedStatus, self, Foe, Value)
            #RanNumber = random.randint(0, len(CurrentStatus))
            # if PickedStatus != "Stun" and PickedStatus != "Freeze":
            #     StatusFunctions[PickedStatus](self, Foe, Value)
            # else:
            #     StatusFunctions[PickedStatus](Value, Foe, self)
        return [PickedStatus, StatusStacks]


def StatusInterp(Status, Player, Foe, Value): #Ultimately this is where a super generalized any status gain/loss check should be able to go
    StatusFunctions = {
            "Thorns": GainThorns,
            "Freeze": GainFreeze,
            "Regen": GainRegen,
            "Poison": GainPoison,
            "Stun": GainStun,
            "Riptide": GainRiptide,
            "Acid": GainAcid,
            "Purity": GainPurity,
        }
    Player.PreventStatusGain = False
    Player.Search("PreventStatusGain")
    if Status != "null" and not Player.PreventStatusGain:
        StatusFunctions[Status](Player, Foe, Value)

        if Status not in Player.StatusesGained:
            Player.StatusesGained = Player.StatusesGained.append(Status)
            Player.Search("FirstGainStatus", Foe)

        if Value > 0 and "RiverflowTalisman" in Player.Items:
            StatusFunctions[Status](Player, Foe, 1)
    

def DealDamage(Damagevalue, Player, Foe):
    if Damagevalue > 0:
        Foe.CurrentHP = min(Foe.CurrentHP, Foe.CurrentHP + Foe.Armor - Damagevalue) #Updates hp of foe if foe's armor reached 0
        Player.TempBombBonus = 0
        Player.BombMult = 1
        HP1Check(Foe, Player)
        if Foe.Armor > 0:
            Foe.DeltaArmor = max(min(Foe.Armor, Damagevalue), 0)
            ArmorLose(Foe, Player)
            Foe.DeltaArmor = 0
            Foe.Armor = max(0, Foe.Armor - Damagevalue)
        Nonweapon(Player, Foe)
        TakeDamage(Foe, Player)

    # if Foe.Armor - Damagevalue >= 0 and Foe.Armor != 0:
    #     Foe.Armor = Foe.Armor - Damagevalue #Updates foe's armor to be old armor - self attack
    #     TakeDamage(Foe, Player) #Add TakeDamage check
    #     #Foe.Exposed(Player)
    # else:
    #     Foe.CurrentHP = Foe.CurrentHP + Foe.Armor - Damagevalue #Updates hp of foe if foe's armor reached 0
    #     Foe.Armor = 0
    #     TakeDamage(Foe, Player) #Add TakeDamage check
    #     #Foe.Wounded(Player) #have you wounded the foe?
    #     #Foe.Exposed(Player)

#Write ItemsEffect("VampireWine") runs +4 to self hp
def ItemsEffect(Phase, Name, Player, Foe):
    if Name == "ArcaneBell":  #Decrease all cooldowns by 1.
        Player.CooldownReduction = Player.CooldownReduction + 1
        Symphony(Player, Foe, "ArcaneBell")

    if Name == "ArcaneBellS":  #Decrease all cooldowns by 1.
        Player.CooldownReduction = Player.CooldownReduction + 1

    if Name == "CherryBomb": #Deals 1 damage 2 times
            BombDamage(1, Player, Foe)
            BombDamage(1, Player, Foe)

    if Name == "CitrineEarring":  #Gain 1 Speed every other turn
        #Player.Speed = Player.Speed + 1
        Player.DeltaSpeed = 1
        GainSpeed(Player, Foe, 1)

    if Name == "CitrineRing": #Possible they die and it doesnt end calc
        for nn in range(0, Player.RingTrigger):
            if Player.Speed > 0:
                DealDamage(Player.Speed, Player, Foe)

    if Name == "ClearspringFeather":  #Decrease a random status effect by 1 and give it to the foe......
        [Status, Stacks] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect
        if Stacks > 0:
            StatusInterp(Status, Foe, Player, 1)

    if Name == "ClearspringWatermelon":  #Decrease a random status effect by 1
        [Status, Stacks] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect

    if Name == "CrackedWhetstone":  #Gain 2 attack for the first turn only
        Player.TempAttack = Player.TempAttack + 2

        # if Player.FirstTurn:
        #     Player.Attack = Player.Attack + 2
        # else:
        #     Player.Attack = Player.Attack - 2

    #if Name == "DeviledEgg" : {"Unique", "Sanguine"}, #Does Nothing

    if Name == "DoublePlatedArmor":
        #Player.Armor = Player.Armor + 3
        #Player.GainedArmor = True
        #Runs check for gained armor items
        ArmorGain(Player, Foe, 3)

    if Name == "EmeraldEarring": #Restore 1 hp
        HealingCalc(Player, Foe, 1)

    if Name == "EmeraldRing":
        for nn in range(0, Player.RingTrigger):
            HealingCalc(Player, Foe, 3)

    if Name == "EmergencyShield": #Less speed than enemy, give 5 armor
        if Player.Speed < Foe.Speed:
            #Player.Armor = Player.Armor + 5
            ArmorGain(Player, Foe, 5)

    if Name == "FrostbiteGauntlet": #Give the enemy 1 Freeze
        StatusInterp("Freeze", Foe, Player, 1)
        #Freeze(1, Player, Foe)
        
    if Name == "FrostbiteTrap": #Give the enemy 2 freeze
        StatusInterp("Freeze", Foe, Player, 2)
        #Freeze(2, Player, Foe)

    if Name == "GraniteEgg":  #Does Nothing
        Player.Armor = Player.Armor

    if Name == "GraniteTome":  #CD 4: Gain 6 armor
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(4*Player.CooldownMult) and Player.GraniteTome) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                ArmorGain(Player, Foe, 6)
                Cooldowned(Player, Foe)
            Player.GraniteTome = False

    if Name == "HolyTome":  #CD 4: Gain 3 attack
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(4*Player.CooldownMult) and Player.HolyTome) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                Player.Attack = Player.Attack + 3
                Cooldowned(Player, Foe)
            Player.HolyTome = False

    if Name == "HornedHelmet": #Gain 1 thorn
        StatusInterp("Thorns", Player, Foe, 1)
        #GainThorns(Player, Foe, 1)

    if Name == "IceblockShield": #Self freeze 2
        StatusInterp("Freeze", Player, Foe, 2)
        #Freeze(2, Foe, Player)

    if Name == "IronstoneBracelet": #Foe strikes deal 1 less damage if you have armor, else +1
        if Player.Armor > 0:
            Foe.TempAttack = Foe.TempAttack - 1
        else:
            Foe.TempAttack = Foe.TempAttack + 1

    if Name == "LifebloodHelmet": #On First turn restore hp = damage from strikes
        HealingCalc(Player, Foe, Foe.DamageFromFoeStrike)

    if Name == "LiferootGauntlet": #Gain 1 Regen
        StatusInterp("Regen", Player, Foe, 1)
        #GainRegen(Player, Foe, 1)

    if Name == "LiferootTome":  #CD 4: Gain 3 regen
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(4*Player.CooldownMult) and Player.LiferootTome) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                StatusInterp("Regen", Player, Foe, 3)
                #GainRegen(Player, Foe, 3)
                Cooldowned(Player, Foe)
            Player.LiferootTome = False

    if Name == "LightspeedPotion": #BatStart Restore HP = Speed
        if Player.Speed > 0:
            HealingCalc(Player, Foe, Player.Speed)

    if Name == "LightspeedElixir": #BatStart gain max hp and Restore HP = Speed
        if Player.Speed > 0:
            Player.MaxHP = Player.MaxHP + Player.Speed
            #Player.Wounded(Foe) #Idk if can cause wounded
            HealingCalc(Player, Foe, Player.Speed)

    if Name == "MusclePotion":  #Every 3 strikes gain 1 attack
        if Player.StrikeCounter%3 == 0:
            Player.Attack = Player.Attack + 1

    if Name == "MuscleElixir":  #Every 3 strikes gain 1 attack, 1 armor, and 1 speed
        if Player.StrikeCounter%3 == 0:
            Player.Attack = Player.Attack + 1
            ArmorGain(Player, Foe, 1)
            GainSpeed(Player, Foe, 1)

    if Name == "PetrifyingFlask": #Wounded: Gain 10 armor and 2 stun
        ArmorGain(Player, Foe, 10)
        StatusInterp("Stun", Player, Foe, 2)
        #Stun(2, Foe, Player)

    if Name == "PetrifyingElixir": #Wounded: Gain 10 armor and stun everyone for 2 turns
        ArmorGain(Player, Foe, 10)
        StatusInterp("Stun", Player, Foe, 2)
        StatusInterp("Stun", Foe, Player, 2)
        #Stun(2, Foe, Player)
        #Stun(2, Player, Foe)

    if Name == "PowderPlate": #Give Foe 2 powder 
        Foe.Powder = Foe.Powder + 2

    if Name == "PurelakeHelmet": #BatStart: Gain 1 Purity
        StatusInterp("Purity", Player, Foe, 1)
        #GainPurity(Player, Foe, 1)

    if Name == "RedwoodCloak": #If on BatStart hp not full, restore 2
        if Healable(Player):
            HealingCalc(Player, Foe, 2)
            # x = Player.CurrentHP - Player.MaxHP + 2
            # Player.CurrentHP = min(Player.MaxHP, Player.CurrentHP + 2)
            # HPRestored(Player, Foe) #Adds check if have an item with effect from hp healing
            # if "HPOverHeal" in Player.Items and x > 0:
            #     DealDamage(x, Player, Foe)

    if Name == "RedwoodHelmet": #Restore 3 hp on exposed
        HealingCalc(Player, Foe, 3)

    if Name == "RoyalHorn":  #Wounded: Gain 2 gold symphony
        Player.Gold = Player.Gold + 2
        Symphony(Player, Foe, "RoyalHorn")

    if Name == "RoyalHornS":  #Wounded: Gain 2 gold symphony
        Player.Gold = Player.Gold + 2

    if Name == "RubyEarring": #Deal 1 damage eot
        DealDamage(1, Player, Foe)

    if Name == "RubyRing":  #Gain 2 attack and take 3 damage
        for nn in range(0, Player.RingTrigger):
            Player.Attack = Player.Attack + 2
            SelfArmorLose(Player, Foe, 3)
        # if SelfArmorLose(Player):
        #     Player.CurrentHP = min(Player.CurrentHP, Player.CurrentHP + Player.Armor - 3) #Updates hp of foe if foe's armor reached 0
        #     if Player.Armor > 0:
        #         ArmorGain(Player, Foe)
        #     TakeDamage(Player, Foe)
        # else:
        #     DealDamage(3, Foe, Player)

    if Name == "RustyRing": #Give the foe 1 acid
        StatusInterp("Acid", Foe, Player, 1)
        #GainAcid(Foe, Player, 1)

    if Name == "SaffronFeather": #Convert 1 speed to 2 hp even if cannot heal?
        if Player.Speed > 0:
            Player.Speed = Player.Speed - 1
            HealingCalc(Player, Foe, 2)

    if Name == "SanguineTome":  #CD 6: Full heal
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(6*Player.CooldownMult) and Player.SanguineTome) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                Sanguine(Player, Foe, Player.MaxHP - Player.CurrentHP)
                Cooldowned(Player, Foe)
            Player.SanguineTome = False


    if Name == "SapphireEarring": #Gain 1 armor eot
        #Player.Armor = Player.Armor + 1
        ArmorGain(Player, Foe, 1)

    if Name == "SapphireRing": #Steal 2 armor from foe (if possible)
        for nn in range(0, Player.RingTrigger):
            if Foe.Armor > 0: #and no towershield triggers?
                Foe.Armor = Foe.Armor - min(Foe.Armor, 2)
                Foe.DeltaArmor = min(Foe.Armor, 2)
                ArmorLose(Foe, Player) #Armor loss for foe
                Foe.DeltaArmor = 0
                #Player.Armor = Player.Armor + min(Foe.Armor, 2)
                ArmorGain(Player, Foe, min(Foe.Armor, 2))

    if Name == "SerpentLyre": #Give the foe 3 poison
        StatusInterp("Poison", Foe, Player, 3)
        #GainPoison(Foe, Player, 3)
        Symphony(Player, Foe, "SerpentLyre")

    if Name == "SerpentLyreS": #Give the foe 3 poison
        StatusInterp("Poison", Foe, Player, 3)
        #GainPoison(Foe, Player, 3)

    if Name == "SilverscaleFish":  #Give the foe 1 riptide
        StatusInterp("Riptide", Foe, Player, 1)
        #GainRiptide(Foe, Player, 1)

    if Name == "SilverscaleTome": #CD 3: Give the foe 2 riptide
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(3*Player.CooldownMult) and Player.SilverscaleTome) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                StatusInterp("Riptide", Foe, Player, 2)
                #GainRiptide(Player, Foe, 2)
                Cooldowned(Player, Foe)
            Player.SilverscaleTome = False

    if Name == "SlimeArmor": #Gain 1 acid
        StatusInterp("Acid", Player, Foe, 1)
        #GainAcid(Player, Foe, 1)

    if Name == "SourLemon": #Gain 1 acid
        StatusInterp("Acid", Player, Foe, 1)
        #GainAcid(Player, Foe, 1)

    if Name == "SpinyChestnut": #Gain 3 thorns
        StatusInterp("Thorns", Player, Foe, 3)
        #GainThorns(Player, Foe, 3)

    if Name == "StormcloudTome": #CD 4: Stun foe 1 turn
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(4*Player.CooldownMult) and Player.StormcloudTome) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                StatusInterp("Stun", Foe, Player, 1)
                #Stun(1, Player, Foe)
                Cooldowned(Player, Foe)
            Player.StormcloudTome = False

    if Name == "SwiftstrikeBelt": #Take 3 damage gain 1 strike on next turn
        GainStrikes(Player, Foe, 1)
        SelfArmorLose(Player, Foe, 3)
        
        # if SelfArmorLose(Player):
        #     Player.CurrentHP = min(Player.CurrentHP, Player.CurrentHP + Player.Armor - 3)
        #     if Player.Armor > 0:
        #         ArmorGain(Player, Foe)
        #     TakeDamage(Player, Foe)
        # else:
        #     DealDamage(3, Foe, Player)

    if Name == "TreebarkEgg":  #Does Nothing
        Player.Armor = Player.Armor

    if Name == "VampireWine":
        Sanguine(Player, Foe, 4)

    if Name == "VenomousFang":  #First Turn: Give foe 2 poison OH
        StatusInterp("Poison", Foe, Player, 2)
        #GainPoison(Foe, Player, 2)

    if Name == "WeaverShield":  #If you have 0 base armor, gain 4 armor
        if Player.BaseArmor == 0:
            ArmorGain(Player, Foe, 4)

    if Name == "WetEgg":  #Does Nothing
        Player.Armor = Player.Armor

    if Name == "ArcaneShield":  #When a countdown effect triggers, gain 3 armor 
        ArmorGain(Player, Foe, 3)

    if Name == "BasiliskScale":  #BatStart: Gain 5 armor and 5 poison
        ArmorGain(Player, Foe, 5)
        StatusInterp("Poison", Player, Foe, 5)
        #GainPoison(Player, Foe, 5)

    if Name == "BigBoom":  #If Foe is at or below 50%, deal 20 damage
        if Foe.CurrentHP/Foe.MaxHP <= 0.5:
            BombDamage(20, Player, Foe)

    if Name == "BlackbriarGauntlet": #Gain 2 thorns per armor lost from foe's first strike
        if Foe.FirstStrike:
            StatusInterp("Thorns", Player, Foe, 2*Player.DeltaArmor)
            #GainThorns(Player, Foe, 2*Player.DeltaArmor)

    if Name == "BlackbriarRose": #Whenever you restore hp gain 2 thorns
        StatusInterp("Thorns", Player, Foe, 2)
        #GainThorns(Player, Foe, 2)

    if Name == "BlastcapArmor":  #Take 5 Damage
        SelfBombDamage(5, Player, Foe)

    if Name == "BombBag": #Spend 3 speed to retrigger a random bomb
        if Player.Speed > 2:
            #Idk if it takes speed if you have no bombs
            #Player.Speed = Player.Speed - 3
            GainSpeed(Player, Foe, -3)
            Player.RandomSearch("Bomb", Foe)

    if Name == "BrambleBelt":  #Gain 2 thorns and give the foe 1 more strike
        StatusInterp("Thorns", Player, Foe, 2)
        #GainThorns(Player, Foe, 2)
        GainStrikes(Foe, Player, 1)

    if Name == "BrambleBuckler": #Convert 1 armor to 2 thorns
        if Player.Armor >= 1: 
            SelfArmorLose(Player, Foe, 1) #Trigger SelfArmorLose
            StatusInterp("Thorns", Player, Foe, 2)
            #GainThorns(Player, Foe, 2)

    if Name == "BrambleTalisman":  #Whenever you gain thorns, gain 1 armor
        ArmorGain(Player, Foe, 1)

    if Name == "BrambleVest":  #The first time you lose thorns, restore hp = to lost thorns
        if Player.Thorns > 0 and Player.FirstThornLose:
            HealingCalc(Player, Foe, Player.ThornsDecrease)

    if Name == "RazorvineTalisman": #When gain thorns, gain another one
        Player.Thorns = Player.Thorns + 1
        #Might need to add thorn gain check in Future

    if Name == "BrittlebarkBuckler": #After Foe's First Strike take damage then lose all armor Probably can just put it as a check directly in the strike calc
        if Player.NoBBB:
            if Player.Armor > 0:
                SelfArmorLose(Player, Foe, Player.Armor)

    if Name == "CausticTome":  #CD 3: Give the foe 3 acid, unless they have no armor, then give 3 poison
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(3*Player.CooldownMult) and Player.CausticTome) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                if Foe.Armor > 0:
                    StatusInterp("Acid", Foe, Player, 3)
                    #GainAcid(Foe, Player, 3)
                elif Foe.Armor == 0:
                    StatusInterp("Poison", Foe, Player, 3)
                    #GainPoison(Foe, Player, 3)
                Cooldowned(Player, Foe)
            Player.CausticTome = False

    if Name == "ChainmailCloak":  #If you have armor restore 2 hp
        if Player.Armor > 0:
            HealingCalc(Player, Foe, 2)

    if Name == "ClearspringCloak": #Remove all status effects and gain 1 armor per stack removed
        if Player.Thorns > 0: 
            x = Player.Thorns
            StatusInterp("Thorns", Player, Foe, -Player.Thorns)
            ArmorGain(Player, Foe, x)

        if Player.Freeze > 0: 
            x = Player.Freeze
            StatusInterp("Freeze", Player, Foe, -Player.Freeze) 
            ArmorGain(Player, Foe, x)

        if Player.Regen > 0: 
            x = Player.Regen
            StatusInterp("Regen", Player, Foe, -Player.Regen)
            ArmorGain(Player, Foe, x) 
            
        if Player.Poison > 0: 
            x = Player.Poison
            StatusInterp("Poison", Player, Foe, -Player.Poison)
            ArmorGain(Player, Foe, x)

        if Player.Stun > 0: 
            x = Player.Stun
            StatusInterp("Stun", Player, Foe, -Player.Stun)
            ArmorGain(Player, Foe, x)
            
        if Player.Riptide > 0: 
            x = Player.Riptide
            StatusInterp("Riptide", Player, Foe, -Player.Riptide)
            ArmorGain(Player, Foe, x)
            
        if Player.Acid > 0: 
            x = Player.Acid
            StatusInterp("Acid", Player, Foe, -Player.Acid)
            ArmorGain(Player, Foe, x)


        if Player.Purity > 0:
            x = Player.Purity 
            StatusInterp("Purity", Player, Foe, -Player.Purity)
            ArmorGain(Player, Foe, x)
            #GainPurity(Player, Foe, -Player.Purity)

    if Name == "ClearspringOpal":  #TS: Spend 1 speed to decrease a random status effect by 1
        if Player.Speed > 0:
            GainSpeed(Player, Foe, -1)
            [Status, Stacks] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect

    if Name == "ClearspringRose":  #Whenever you restore hp, decrease a random status effect by 1.
        [Status, Stacks] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect

    if Name == "CorrodedBone":  #Convert 50% of Enemies hp into Armor. Rounded down?
        #Might not count as damage?
        if np.floor(Foe.CurrentHP/2) > 0:
            ArmorGain(Foe, Player, np.floor(Foe.CurrentHP/2))
            Foe.CurrentHP = np.ceil(Foe.CurrentHP/2)
            TakeDamage(Foe, Player) #Might be missing smth

    if Name == "CrackedBouldershield": #Gain 7 armor
        #Player.Armor = Player.Armor + 7
        ArmorGain(Player, Foe, 7)

    if Name == "CrimsonFang":  #If your hp is full, lose 5 hp and gain 2 strikes
        if Player.MaxHP == Player.CurrentHP:
            Player.CurrentHP = Player.CurrentHP - 5
            HP1Check(Player, Foe)
            GainStrikes(Player, Foe, 2)
            TakeDamage(Player, Foe)

    if Name == "EnergyDrain": #steal all foe's speed
        if Foe.Speed > 0: #Player.Speed == 0 and 
            #Player.Speed = np.copy(Foe.Speed)
            Player.DeltaSpeed = np.copy(Foe.Speed)
            GainSpeed(Player, Foe, Foe.Speed)
            Foe.Speed = 0

    if Name == "ExplosivePowder":  #All bomb items deal 1 more damage
        Player.BombBonus = Player.BombBonus + 1

    if Name == "ExplosiveSurprise": #Deal 6 damage
        for nn in range(1, Player.Bombtrigger):
            BombDamage(6, Player, Foe)
            # DealDamage(6 + Foe.Powder, Player, Foe)
            # Foe.Powder = max(0, Foe.Powder - 1)

    if Name == "FeatherweightArmor": #Gain 2 armor for every gained speed
        #Player.Armor = Player.Armor + 2*Player.DeltaSpeed
        ArmorGain(Player, Foe, Player.DeltaSpeed)

    if Name == "FeatherweightGauntlet":  #Spend 2 speed to gain 4 attack temp
        GainSpeed(Player, Foe, -2)
        Player.TempAttack = Player.TempAttack + 4

    if Name == "FeatherweightGreaves": #If you have 0 speed, gain 2 speed
        if Player.Speed == 0:
            Player.DeltaSpeed = 2
            GainSpeed(Player, Foe, 2)

    if Name == "FeatherweightHelmet": #Spend 2 armor and gain 3 speed and 1 attack
        if Player.Armor >= 2:
            #Player.Armor = Player.Armor - 2
            SelfArmorLose(Player, Foe, 2) #Trigger SelfArmorLosecheck and then damage
            #Player.Speed = Player.Speed + 3
            Player.DeltaSpeed = 3
            GainSpeed(Player, Foe, 3)
            Player.Attack = Player.Attack + 1

    if Name == "FirecrackerBelt": #Deal 1 damage 4 times
        for nn in range(1, Player.Bombtrigger):
            for i in range(0, 4):
                BombDamage(1, Player, Foe)
                # DealDamage(1 + Foe.Powder, Player, Foe)
                # Foe.Powder = max(0, Foe.Powder - 1)

    if Name == "FlameburstTome":  #CD 4: Deal 4 and reset cooldown
        if (Player.Cooldown%(np.ceil(4*Player.CooldownMult) - Player.CooldownReduction) == 0) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                BombDamage(4, Player, Foe)
                Cooldowned(Player, Foe)


    if Name == "ForgeGauntlet":  #Give the foe 5 armor
        ArmorGain(Foe, Player, 5)

    if Name == "FortifiedGauntlet":#If you have armor, gain an armor
        if Player.Armor > 0:
            #Player.Armor = Player.Armor + 1
            ArmorGain(Player, Foe, 1)

    if Name == "FrostbiteArmor":  #Enemy's first strike does 2x, then give them 4 freeze
        StatusInterp("Freeze", Foe, Player, 4)
        #Freeze(4, Foe, Player)

    if Name == "FrostbiteCurse": #Give yourself and foe 5 freeze each
        StatusInterp("Freeze", Player, Foe, 5)
        StatusInterp("Freeze", Foe, Player, 5)
        #Freeze(5, Player, Foe)
        #Freeze(5, Foe, Player)  

    if Name == "GoldRing": #Gain 1 gold RING
        for nn in range(0, Player.RingTrigger):
            Player.Gold = Player.Gold + 1

    if Name == "GraniteCrown": #Gain max HP = to Base armor
        Player.MaxHP = Player.MaxHP + Player.BaseArmor
        #MaxHPGain? It can cause wounded to trigger
        Player.Wounded(Foe)

    if Name == "GraniteFungi": #Gain 2 armor to you and foe
        ArmorGain(Player, Foe, 2)
        ArmorGain(Foe, Player, 2)

    if Name == "HeartshapedAcorn": #If you have 0 base armor set HP to MaxHP
        if Player.BaseArmor == 0 and Player.MaxHP > Player.CurrentHP:
            #Could need smth for twilightcrest Idk
            Player.CurrentHP = Player.MaxHP
            HPRestored(Player, Foe)

    if Name == "HeartshapedPotion": #When reaching exactly 1 hp first time restore HP to MaxHP (Need to add every that loses hp)
        if Player.HP1PotionTrigger:
            if Player.MaxHP > 1:
                Player.HP1PotionTrigger = False
                Sanguine(Player, Foe, Player.MaxHP - 1)

    if Name == "HeartshapedElixir":  #When reaching below 5 hp first time restore HP to MaxHP (Need to add every that loses hp)
        if Player.HP1ElixirTrigger:
            if Player.MaxHP > 1:
                Player.HP1ElixirTrigger = False
                Sanguine(Player, Foe, Player.MaxHP - Player.CurrentHP)


    if Name == "IceSpikes":  #If you have freeze, gain 5 thorns
        if Player.Freeze > 0:
            StatusInterp("Thorns", Player, Foe, 5)
            #GainThorns(Player, Foe, 5)

    if Name == "IceTomb":  #If you have armor, gain 3 armor and 1 freeze.
        if Player.Armor > 0:
            ArmorGain(Player, Foe, 3)
            StatusInterp("Freeze", Player, Foe, 1)
            #Freeze(1, Foe, Player)

    if Name == "ImpressivePhysique": #Exposed: Stun the foe for 1 turn
        StatusInterp("Stun", Foe, Player, 1)
        #Stun(1, Player, Foe)

    if Name == "IronRose":
        #Player.Armor = Player.Armor + 1
        ArmorGain(Player, Foe, 1) #Runs check for gained armor items

    if Name == "IronShrapnel": #Deal 3 damage to foe if has armor. else deal 2x
        #for nn in range(1, Player.Bombtrigger):
        if Foe.Armor > 0:
            BombDamage(3, Player, Foe)
            # DealDamage(3 + Foe.Powder, Player, Foe)
            # Foe.Powder = max(0, Foe.Powder - 1)
        elif Foe.Armor == 0:
            Player.BombMult = 2*Player.BombMult
            BombDamage(3, Player, Foe)

    if Name == "IronstoneSandals": #Gain 3 attack when have armor
        if Player.Armor > 0:
            Player.TempAttack = Player.TempAttack + 3

    if Name == "KindlingBomb":  #Deal 1 damage, then give the next bomb a temp damage increase.
        BombDamage(1, Player, Foe)
        Player.TempBombBonus = Player.TempBombBonus + 3
        

    if Name == "LeatherBoots":#More speed than foe, gain 2 attack
        if Foe.Speed < Player.Speed:
            Player.Attack = Player.Attack + 2

    if Name == "LeatherWaterskin": #Gain 2 purity, repeat for each equipped water item
        c = Count(Player, "Water")
        for nn in range(0, c + 1):
            StatusInterp("Purity", Player, Foe, 2)
            #GainPurity(Player, Foe, 2)

    if Name == "LightningBottle": #Stun yourself for 1 turn
        StatusInterp("Stun", Player, Foe, 1)
        #Stun(1, Foe, Player)

    if Name == "LightningElixir":  #Stun yourself for 2 turns
        StatusInterp("Stun", Player, Foe, 2)
        #Stun(2, Foe, Player)

    if Name == "MarshlightLantern": #Lose 3 hp and gain 8 armor
        Player.CurrentHP = Player.CurrentHP - 3
        HP1Check(Player, Foe)
        ArmorGain(Player, Foe, 8)
        TakeDamage(Player, Foe)

    if Name == "MoonlightCrest":  #If you are below 50% hp, gain 1 regen
        if Player.CurrentHP/Player.MaxHP < 0.5:
            StatusInterp("Regen", Player, Foe, 1)
            #GainRegen(Player, Foe, 1)

    if Name == "MuscleGrowth":  #While you have regen, temp gain 3 attack
        if Player.Regen > 0:
            Player.TempAttack = Player.TempAttack + 3

    if Name == "MushroomBuckler":  #If you have poison, foe strikes do 1 less damage
        if Player.Poison > 0:
            Foe.TempAttack = Foe.TempAttack - 1

    if Name == "NervePotion":  #The first time the foe gains poison, give them 1 stun
        if Player.NervePot:
            Player.NervePot = False
            StatusInterp("Stun", Foe, Player, 1)
            #Stun(1, Player, Foe)

    if Name == "NerveElixir": #The first time the foe gains poison, give them 3 stun
        if Player.NerveElixir:
            Player.NerveElixir = False
            StatusInterp("Stun", Foe, Player, 3)
            #Stun(3, Player, Foe)
    
    if Name == "OreHeart": #Gain 3 armor per equipped stone item
        c = Count(Player, "Stone")
        #Player.Armor = Player.Armor + 3*c
        ArmorGain(Player, Foe, 3*c)

    if Name == "PineconeBreastplate": #If HP = max HP at BatStart then gain PineconeBreastplateTS item
        if Player.MaxHP == Player.CurrentHP:
            #Search Player.Items() to replace "PineconeBreastplate" with "PineconeBreastplateTS"
            Player.Items = [word.replace("PineconeBreastplate", "PineconeBreastplateTS") for word in Player.Items]

    if Name == "PineconeBreastplateTS":
        StatusInterp("Thorns", Player, Foe, 1)
        #GainThorns(Player, Foe, 1) #CheckThornsGain 

    if Name == "PlatedGreaves": #Convert 3 speed to 9 armor
        if Player.Speed >= 1:
            ArmorGain(Player, Foe, 3*Player.Speed)
            Player.Speed = Player.Speed - min(Player.Speed, 3)
            #Player.Armor = Player.Armor + 9
            
    if Name == "PoisonousMushroom":  #Gain 1 poison
        StatusInterp("Poison", Player, Foe, 1)
        #GainPoison(Player, Foe, 1)

    if Name == "PurelakeArmor":  #Exposed: Remove 1 purity to gain 5 armor
        if Player.Purity > 0:
            #GainPurity(Player, Foe, -1)
            StatusInterp("Purity", Player, Foe, -1)
            ArmorGain(Player, Foe, 5)

    if Name == "PurelakePotion": #Remove all armor and gain 3 purity
        SelfArmorLose(Player, Foe, Player.Armor)
        StatusInterp("Purity", Player, Foe, 3)
        #GainPurity(Player, Foe, 3)

    if Name == "PurelakeElixir":  #Lose 5 armor and gain 5 purity
        Player.Armor = Player.Armor - min(5, Player.Armor)
        ArmorLose(Player, Foe)
        StatusInterp("Purity", Player, Foe, 5)
        #GainPurity(Player, Foe, 5)

    if Name == "PurelakeTome": #CD 3: if you have purity, remove 1. Else gain 1. Reset cd
        if (Player.Cooldown%(np.ceil(3*Player.CooldownMult) - Player.CooldownReduction) == 0) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeTriggers):
                if Player.Purity > 0:
                    #GainPurity(Player, Foe, -1)
                    StatusInterp("Purity", Player, Foe, -1)
                elif Player.Purity == 0:
                    StatusInterp("Purity", Player, Foe, 1)
                    #GainPurity(Player, Foe, 1)
                Cooldowned(Player, Foe)

    #if Name == "RiverflowTalisman":  #Whenever you gain a status, gain 1 more


    if Name == "RiverflowViolin": #Gain 4 armor
        ArmorGain(Player, Foe, 4)
        Symphony(Player, Foe, "RiverflowViolin")

    if Name == "RiverflowViolinS": #Gain 4 armor
        ArmorGain(Player, Foe, 4)

    if Name == "RoyalHelmet":  #Gain 10 armor IF you have more than 20 gold
        if Player.Gold > 20: #Might work like >= in game
            #Player.Armor = Player.Armor + 10
            ArmorGain(Player, Foe, 10)

    if Name == "RustedPlate":  #If the foe loses armor to acid, you gain that armor
        ArmorGain(Player, Foe, Foe.DeltaArmor)
        Foe.DeltaArmor = 0

    if Name == "SaltcrustedCrown":  #gain 1 riptide
        StatusInterp("Riptide", Player, Foe, 1)
        #GainRiptide(Player, Foe, 1)

    if Name == "SanguineRose": #When healed heal again for 1 hp
        l = 1
        if Player.CurrenHP/Player.MaxHP < 0.5:
            l = Player.TwilightCrestMult
        v = 1
        if Player.Stun > 0: #
            v = Player.VampireCloak
        x = Player.CurrentHP - Player.MaxHP + 1*Player.SanguineMult*l*v*Player.SanguineScepterMult
        if Healable(Player):
            Player.CurrentHP = min(Player.MaxHP, Player.CurrentHP + 1*Player.SanguineMult*l*v*Player.SanguineScepterMult)
            Player.Search("HPRestoredS", Foe)
        if "HPOverHeal" in Player.Items and x > 0:
            DealDamage(x, Player, Foe)

    if Name == "SilverAnchor":  #Whenever you lose speed, give the foe 1 riptide
        StatusInterp("Riptide", Foe, Player, 1)
        #GainRiptide(Foe, Player, 1)

    if Name == "SilverscaleArmor":  #Whenever riptide triggers, gain 2 armor
        ArmorGain(Player, Foe, 2)

    if Name == "SilverscaleGreaves":  #If you have more speed, give foe 2 riptide
        if Player.Speed > Foe.Speed:
            StatusInterp("Riptide", Foe, Player, 2)
            #GainRiptide(Foe, Player, 2)

    if Name == "SinfulMirror": #Remove all your purity
        StatusInterp("Purity", Player, Foe, -Player.Purity)
        #GainPurity(Player, Foe, -Player.Purity)

    if Name == "SlimeBomb":  #Remove all their acid, and deal 2 damage per acid removed
        BombDamage(2*Foe.Acid, Player, Foe) #With powder keg does it really do the damage 3 times?
        StatusInterp("Acid", Foe, Player, -Foe.Acid)
        #GainAcid(Foe, Player, -Foe.Acid)

    if Name == "SlimeBooster":  #Convert 1 acid to 2 attack
        if Player.Acid > 0:
            StatusInterp("Acid", Player, Foe, -1)
            #GainAcid(Player, Foe, -1)
            Player.Attack = Player.Attack + 2

    if Name == "SlimeHeart":  #Remove all your acid and restore 2 hp per acid removed
        if Player.Acid > 0:
            HealingCalc(Player, Foe, 2*Player.Acid)
            StatusInterp("Acid", Player, Foe, -Player.Acid)
            #GainAcid(Player, Foe, -Player.Acid)

    if Name == "SlimePotion":  #Gain armor = missing hp and gain 5 acid.
        ArmorGain(Player, Foe, Player.MaxHP-Player.CurrentHP)
        StatusInterp("Acid", Player, Foe, 5)
        #GainAcid(Player, Foe, 5)

    if Name == "SlimeElixir": #Gain armor = max hp and gain 5 acid.
        ArmorGain(Player, Foe, Player.MaxHP)
        StatusInterp("Acid", Player, Foe, 5)
        #GainAcid(Player, Foe, 5)

    if Name == "SmokeBomb": #If less speed than foe, then gain 3 speed and give foe 3 powder
        #Maybe it only does the check once and then triggers twice??
        #for nn in range(1, Player.Bombtrigger):
        if Player.Speed < Foe.Speed:
            #Player.Speed = Player.Speed + 3
            Player.DeltaSpeed = 3 
            GainSpeed(Player, Foe, 3)
            #Foe.Powder = Foe.Powder + 3

    if Name == "SpiralShell":  #If Stunned, give foe 1 riptide
        if Player.Stun > 0:
            StatusInterp("Riptide", Foe, Player, 1)
            #GainRiptide(Foe, Player, 1)

    if Name == "SpiritualBalance": #If your speed = attack. gain 3 attack
        if Player.Speed == Player.Attack:
            Player.Attack = Player.Attack + 3

    if Name == "StoneSteak": #If HP = MaxHP, gain 5 armor
        if Player.MaxHP == Player.CurrentHP:
            #Player.Armor = Player.Armor + 5
            ArmorGain(Player, Foe, 5)

    if Name == "StormcloudArmor": #If you have more speed than armor, stun foe for 2 turns
        if Player.Speed > Player.Armor:
            StatusInterp("Stun", Foe, Player, 2)
            #Stun(2, Player, Foe)

    if Name == "StormcloudCurse":  #Stun yourself and the foe for 2 turns
        StatusInterp("Stun", Player, Foe, 2)
        StatusInterp("Stun", Foe, Player, 2)
        #Stun(2, Player, Foe)
        #Stun(2, Foe, Player)

    if Name == "SunlightCrest":  #If you're above 50% hp, lose 3 hp and gain 1 attack
        if Player.CurrentHP/Player.MaxHP > 0.5:
            Player.CurrentHP = Player.CurrentHP - 3
            HP1Check(Player, Foe)
            Player.Attack = Player.Attack + 1
            TakeDamage(Player, Foe)

    if Name == "SwiftstrikeCrown":  #Spend 5 speed to perm gain 1 extra strike~~~~~Adds x2 when having the specifc weapon
        if Player.Speed >= 5:
            GainSpeed(Player, Foe, -5)
            Player.BaseStrikesCount = Player.BaseStrikesCount + 1

    if Name == "TempestBreastplate": #Gain speed = base armor
        if Player.BaseArmor > 0:
            #Player.Speed = Player.Speed + Player.BaseArmor 
            Player.DeltaSpeed = Player.BaseArmor
            GainSpeed(Player, Foe, Player.BaseArmor)

    if Name == "ThornRing": #Take 1 damage and gain thorns equal to missing hp
        #DealDamage(1, Foe, Player)
        for nn in range(0, Player.RingTrigger):
            SelfArmorLose(Player, Foe, 1) #Trigger SelfArmorLosecheck and then damage
            if Player.MaxHP - Player.CurrentHP > 0:
                StatusInterp("Thorns", Player, Foe, Player.MaxHP - Player.CurrentHP)
                #GainThorns(Player, Foe, Player.MaxHP - Player.CurrentHP)

    if Name == "ToxicAlgae": #Give the foe 5 poison
        StatusInterp("Poison", Foe, Player, 5)
        #GainPoison(Foe, Player, 5)

    if Name == "ToxicRose": #Whenever you restore hp, give foe 1 poison
        StatusInterp("Poison", Foe, Player, 1)
        #GainPoison(Foe, Player, 1)

    if Name == "TwistedRoot":  #Gain 1 regen per equipped wood
        c = Count(Player, "Wood")
        if c > 0: StatusInterp("Regen", Player, Foe, c)
        #GainRegen(Player, Foe, c)

    if Name == "VampiricStasis": #Whenever you skip your strike, restore 3 HP
        Sanguine(Player, Foe, 3)
        
    if Name == "ViperExtract": #First time foe gains poison, give them 3 more
        if Player.ViperPot:
            Player.ViperPot = False
            StatusInterp("Poison", Foe, Player, 3)
            #GainPoison(Foe, Player, 3)

    if Name == "ViperElixir": #First time foe gains poison, give them 9 more
        if Player.ViperElixir:
            Player.ViperElixir = False
            StatusInterp("Poison", Foe, Player, 9)
            #GainPoison(Foe, Player, 9)

    if Name == "AcidMutation":  #gain 1 Acid
        if Phase == "BattleStart":
            StatusInterp("Acid", Player, Foe, 1)
        if Phase == "PreStrike":
            if Player.Acid > 0:
                Player.TempAttack = Player.TempAttack + Player.Acid
        #GainAcid(Player, Foe, 1)
        #Player.Items = [word.replace("AcidMutation", "AcidMutationPS") for word in Player.Items]
    
    # if Name == "AcidMutationPS":  #Gain temp attack = to acid
    #     if Player.Acid > 0:
    #         Player.TempAttack = Player.TempAttack + Player.Acid

    if Name == "AcidicWitherleaf":  #Give the foe acid = to your speed
        if Player.Speed > 0:
            StatusInterp("Acid", Player, Foe, Player.Speed)
            #GainAcid(Foe, Player, Player.Speed)

    if Name == "AssaultGreaves": #Deal 1 damage
        DealDamage(1, Player, Foe)

    if Name == "BlackbriarArmor": #Whenever you take damage, gain 2 thorns
        StatusInterp("Thorns", Player, Foe, 2)
        #GainThorns(Player, Foe, 2)

    if Name == "BloodstoneRing":  #BS: Gain 5 max hp and restore 5 hp
        for nn in range(0, Player.RingTrigger):
            Player.MaxHP = Player.MaxHP + 5
            #Dont think wounded can trigger?
            #Player.Wounded(Foe)
            Sanguine(Player, Foe, 5)

    if Name == "BrittlebarkArmor":  #Take another damage
        #This might not infinite selfloop
        if Player.NoBBB:
            if "SelfArmorLose" in Player.Items:
                if Player.Armor >= 1:
                    Player.CurrentHP = min(Player.CurrentHP, Player.CurrentHP + Player.Armor - 1) 
                    HP1Check(Player, Foe)
                    Player.DeltaArmor = 1
                    ArmorLose(Player, Foe)
                    #Player.DeltaArmor = 0
                    ArmorGain(Player, Foe, Player.DeltaArmor)
                    Player.DeltaArmor = 0
                    Player.Wounded(Foe) #have you been wounded?
                    Player.Exposed(Foe)
                    Player.Search("TakeDamageS", Foe) #Adds TakeDamage check
                else:
                    Player.CurrentHP = min(Player.CurrentHP, Player.CurrentHP + Player.Armor - 1) 
                    HP1Check(Player, Foe)
                    Player.Armor = max(0, Player.Armor - 1)
                    Player.Wounded(Foe) #have you been wounded?
                    Player.Exposed(Foe)
                    Player.Search("TakeDamageS", Foe) #Adds TakeDamage check

            else:
                Player.CurrentHP = min(Player.CurrentHP, Player.CurrentHP + Player.Armor - 1) 
                HP1Check(Player, Foe)
                if Player.Armor >= 1:
                    Player.DeltaArmor = 1
                    ArmorLose(Player, Foe)
                    Player.DeltaArmor = 0
                Player.Armor = max(0, Player.Armor - 1)
                Player.Wounded(Foe) #have you been wounded?
                Player.Exposed(Foe)
                Player.Search("TakeDamageS", Foe) #Adds TakeDamage check

    if Name == "CactusCap":  #Convert armor to thorns
        if Player.Armor >= 1:
            x = np(Player.Armor)
            SelfArmorLose(Player, Foe, Player.Armor)
            StatusInterp("Thorns", Player, Foe, x)
            #GainThorns(Player, Foe, x)

    if Name == "ChainmailArmor": #RegainBaseArmor
        if Player.BaseArmor > 0:
            #Player.Armor = Player.BaseArmor + Player.Armor
            ArmorGain(Player, Foe, Player.BaseArmor)

    if Name == "ClearspringDuck": #Gain 1 armor and decrease a random status effect by 1
        ArmorGain(Player, Foe, 1)
        [Status, Stacks] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect


    if Name == "CrimsonCloak": #Restore 1 HP
        Sanguine(Player, Foe, 1)

    if Name == "ExplosiveArrow":  #If foe doesnt have armor, deal 2 damage
        if Foe.Armor == 0:
            BombDamage(2, Player, Foe)

    if Name == "GrandTome":  #CD 10: Retriggers all other tomes
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(10*Player.CooldownMult) and Player.GrandTome):
            for nn in range(0, Player.TomeTriggers):
                Player.GrandTome = False
                Player.GrandTomeRetriggers = True
                Player.Search("Tome", Foe)
                Player.GrandTomeRetriggers = False
                Cooldowned(Player, Foe)
            
    if Name == "IronTransfusion": #Gain 2 armor lose 1 hp
        Player.CurrentHP = Player.CurrentHP - 1
        HP1Check(Player, Foe)
        #Player.Armor = Player.Armor + 2
        ArmorGain(Player, Foe, 2)
        TakeDamage(Player, Foe)

    if Name == "IronskinPotion": #Gain armor = missing hp
        if Healable(Player):
            #Player.Armor = Player.Armor + Player.MaxHP - Player.CurrentHP
            ArmorGain(Player, Foe, Player.MaxHP - Player.CurrentHP)

    if Name == "IronskinElixir":  #Double your max hp. Gain armor = missing hp
        Player.MaxHP = 2*Player.MaxHP
        Player.Wounded(Foe)
        ArmorGain(Player, Foe, Player.MaxHP - Player.CurrentHP)

    if Name == "IronstoneArmor":  #Enemy strikes deal 2 less damage while you have armor
        if Player.Armor > 0:
            Foe.TempAttack = Foe.TempAttack - 2

    if Name == "LifeZap": #Lose all your hp except 1 and stun the foe for 2 turns
        if Player.CurrentHP > 1:
            Player.CurrentHP = 1
            HP1Check(Player, Foe)
            TakeDamage(Player, Foe)
        else:
            HP1Check(Player, Foe)
        StatusInterp("Stun", Foe, Player, 2)
        #Stun(2, Foe, Player)

    if Name == "LifebloodArmor": #Convert 50% of current hp rounded down to x armor
        x = np.floor(Player.CurrentHP / 2)
        Player.CurrentHP = Player.CurrentHP - x
        HP1Check(Player, Foe)
        if x > 0:
            TakeDamage(Player, Foe) #Maybe LBA doesnt activate take damage effects
            #Player.Armor = Player.Armor + 2*x
            ArmorGain(Player, Foe, x)

    # if Name == "LifebloodBurst": #Deal 50% rounded down of your hp to foe
    #     DealDamage(np.floor(Player.MaxHP / 2), Player, Foe)

    if Name == "LiferootBeast": #If you have 0 regen, gain 3 regen
        if Player.Regen == 0:
            StatusInterp("Regen", Player, Foe, 3)
            #GainRegen(Player, Foe, 3)

    if Name == "LiferootLute": #Gain 3 regen
        StatusInterp("Regen", Player, Foe, 3)
        #GainRegen(Player, Foe, 3)
        Symphony(Player, Foe, "LiferootLute")

    if Name == "LiferootLuteS": #Gain 3 regen
        StatusInterp("Regen", Player, Foe, 3)
        #GainRegen(Player, Foe, 3)

    if Name == "MoonlightShield": #If you are below 50% hp, gain 2 armor
        if Player.CurrentHP/Player.MaxHP < 0.5:
            ArmorGain(Player, Foe, 2)

    if Name == "NoxiousGas":  #Both you and the foe get 1 poison
        StatusInterp("Poison", Player, Foe, 1)
        StatusInterp("Poison", Foe, Player, 1)
        #GainPoison(Player, Foe, 1)
        #GainPoison(Foe, Player, 1)

    if Name == "OverchargedOrb":  #Stun the foe for 3 turns
        StatusInterp("Stun", Foe, Player, 3)
        #Stun(3, Player, Foe)

    if Name == "PertrifiedStatue":  #Give the foe 1 stun per stone equipped
        StatusInterp("Stun", Foe, Player, Count(Player, "Stone"))
        #Stun(Count(Player, "Stone"), Player, Foe)

    if Name == "PlatedHelmet": #If below 50% hp, gain 2 armor
        if Player.MaxHP/2 > Player.CurrentHP:
            #Player.Armor = Player.Armor + 2
            ArmorGain(Player, Foe, 2)

    if Name == "PurelakeChalice": #Gain 1 purity eot
        StatusInterp("Purity", Player, Foe, 1)
        #GainPurity(Player, Foe, 1)

    if Name == "RazorBreastplate":  #Gain thorns = foe's attack
        if Foe.Attack > 0: #Idk if you can gain negative thorns
            StatusInterp("Thorns", Player, Foe, Foe.Attack)
            #GainThorns(Player, Foe, Foe.Attack)

    # if Name == "PowderKeg": #Give foe 1 powder
    #     Foe.Powder = Foe.Powder + 1

    if Name == "RoyalShield": #Convert 1 gold to 3 armor
        if Player.Gold > 0:
            Player.Gold = Player.Gold - 1
            ArmorGain(Player, Foe, 3)

    if Name == "RubyGemstone": #If your attack is 1, deal 4 extra damage
        if Player.Attack == 1:
            DealDamage(4, Player, Foe)
            #Nonweapon damagecheck

    if Name == "SanguineImp": #Deal 1 damage and restore 1 hp
        DealDamage(1, Player, Foe)
        Sanguine(Player, Foe, 1)

    if Name == "SanguineMorphosis":  #Stun yourself and gain 3 regen
        if Player.TurnCounter%4 == 0:
            StatusInterp("Stun", Player, Foe, 1)
            #Stun(1, Foe, Player)
            StatusInterp("Regen", Player, Foe, 3)
            #GainRegen(Player, Foe, 3)

    if Name == "SapphireGemstone": #When ever you lose armor restore than much hp
        if Player.CurrentHP/Player.MaxHP < 0.5:
            Player.DeltaArmor = Player.DeltaArmor*Player.TwilightCrestMult
        if Player.Stun > 0:
            Player.DeltaArmor = Player.DeltaArmor*Player.VampireCloak
        x = (Player.CurrentHP + Player.DeltaArmor*Player.SanguineScepterMult) - Player.MaxHP #Overheal Value
        if Healable(Player):
            Player.CurrentHP = max(Player.MaxHP, Player.CurrentHP + Player.DeltaArmor*Player.SanguineScepterMult)
            Player.DeltaArmor = 0
            HPRestored(Player, Foe)
        if "HPOverHeal" in Player.Items and x > 0:
            Player.DeltaArmor = 0
            DealDamage(x, Player, Foe)

    if Name == "SerpentMask": #Give the foe poison = to attack
        StatusInterp("Poison", Foe, Player, Player.Attack + Player.TempAttack)
        #GainPoison(Foe, Player, Player.Attack + Player.TempAttack)

    if Name == "SheetMusic":  #CD 6: Trigger Symphony 3 times
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(6*Player.CooldownMult) and Player.SheetMusic) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.SheetMusic):
                for mm in range(0, 3):
                    Symphony(Player, Foe, "")
                Cooldowned(Player, Foe)
            Player.SheetMusic = False
        
    if Name == "ShieldTalisman":
        Player.Armor = Player.Armor + 1
        Player.GainedArmor = True
        #Player.Search("ArmorGainS", Foe)

    if Name == "SilverscaleGauntlet": #Give 1 riptide eot
        StatusInterp("Riptide", Foe, Player, 1)
        #GainRiptide(Foe, Player, 1)

    if Name == "StonebornTurtle": #Restore 1 hp, unless hp is full then gain 2 armor
        if Player.MaxHP > Player.CurrentHP:
            HealingCalc(Player, Foe, 1)
        elif Player.MaxHP == Player.CurrentHP:
            ArmorGain(Player, Foe, 2)

    if Name == "StormcloudDrum": #Give the foe 1 stun
        StatusInterp("Stun", Foe, Player, 1)
        #Stun(1, Player, Foe)
        Symphony(Player, Foe, "StormcloudDrum")

    if Name == "StormcloudDrumS": #Give the foe 1 stun
        StatusInterp("Stun", Foe, Player, 1)
        #Stun(1, Player, Foe)

    if Name == "StuddedGauntlet": #Deal 1 damage
        DealDamage(1, Player, Foe)

    if Name == "SwiftstrikeCloak": #If you have more speed than foe, gain an additional strike
        if Player.Speed > Player.Foe:
            GainStrikes(Player, Foe, 1)

    if Name == "SwiftstrikeGauntlet": #Gain 2 additional strikes next turn
        GainStrikes(Player, Foe, 2)

    if Name == "SwordTalisman": #deal 1 more damage
        Foe.CurrentHP = min(Foe.CurrentHP, Foe.CurrentHP + Foe.Armor - 1) #Updates hp of foe if foe's armor reached 0
        HP1Check(Foe, Player)
        if Foe.Armor > 0:
            Foe.DeltaArmor = max(min(Foe.Armor, 1), 0)
            ArmorLose(Foe, Player)
            Foe.DeltaArmor = 0
            Foe.Armor = max(0, Foe.Armor - 1)
        TakeDamage(Foe, Player)

    if Name == "TimeBomb":  #Exposed deal 1 damage. This item does 2 more damage for each start turn passed.
        BombDamage(1 + 2*Player.TurnCounter, Player, Foe)

    if Name == "TomeOfTheHero": #CD 8: Gain 4 attack, 4 armor, and 4 speed
        if (Player.Cooldown + Player.CooldownReduction < np.ceil(8*Player.CooldownMult) and Player.TomeOfTheHero) or Player.GrandTomeRetriggers:
            for nn in range(0, Player.TomeOfTheHero):
                Player.Attack = Player.Attack + 4
                ArmorGain(Player, Foe, 4)
                GainSpeed(Player, Foe, 4)
                Cooldowned(Player, Foe)
            Player.TomeOfTheHero = False

    if Name == "WeaverArmor": #If you have 0 base armor, gain armor = current hp
        if Player.BaseArmor == 0:
            ArmorGain(Player, Foe, Player.CurrentHP)

    # if Name == "FeatherweightGreaves": #Lose all speed and deal 2 damage per speed lost
    #     if Player.Speed > 0:
    #         x = np.copy(Player.Speed)
    #         Player.Speed = 0
    #         DealDamage(2*x, Player, Foe)

    if Name == "GraniteThorns": #Needs a counter to not remove thorns
        Player.ThornsTriggers = 3

    if Name == "RazorScales": #If you lose armor, deal damage
        x = np.copy(Player.DeltaArmor)
        Player.DeltaArmor = 0 #Changing to 0 first prevents possible random loops
        DealDamage(x, Player, Foe) 

    if Name == "BitterMelon":  #Convert 1 stack of another status effect to 1 poison
        [Status, Stacks] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect
        if Stacks > 0:
            StatusInterp("Poison", Player, Foe, 1)
            #GainPoison(Player, Foe, 1)

    if Name == "BloodOrange":  #Gain 3 acid
        if Phase == "Wounded":
            if Player.Acid > 0:
                x = Player.Acid
                StatusInterp("Acid", Player, Foe, -Player.Acid)
                StatusInterp("Regen", Player, Foe, x)
            
        if Phase == "BattleStart":
            StatusInterp("Acid", Player, Foe, 3)

    # if Name == "BloodOrange":  #Gain 3 acid
    #     StatusInterp("Acid", Player, Foe, 3)
    #     #GainAcid(Player, Foe, 3)
    #     replaced = False
    #     for jj in range(0, len(Player.Items)):
    #         if not replaced and Player.Items[jj] == "BloodOrange":
    #             Player.Items[jj] = "BloodOrangeW"
    #             replaced = True
            
    # if Name == "BloodOrangeW":  #Convert all acid to regen
    #     #Probably doesnt count as sanguine healing surely
    #     if Player.Acid > 0:
    #         x = Player.Acid
    #         StatusInterp("Acid", Player, Foe, -Player.Acid)
    #         StatusInterp("Regen", Player, Foe, x)

    if Name == "BloodSausage":  #Restore 1 hp 5 times
        for i in range(0, 5):
            Sanguine(Player, Foe, 1)

    if Name == "BloodySteak" : #Restore 10 hp and 5 armor
        HealingCalc(Player, Foe, 10)
        #Player.Armor = Player.Armor + 5
        ArmorGain(Player, Foe, 5)

    if Name == "BoiledHam": #Decrease all status effects by 1
        if Player.Thorns > 0: 
            #Player.Thorns = Player.Thorns - 1 
            StatusInterp("Thorns", Player, Foe, -1)
            #ThornsLose(Player, Foe, 1)

        if Player.Freeze > 0: 
            StatusInterp("Freeze", Player, Foe, -1) #Freeze(-1, Foe, Player)

        if Player.Regen > 0: 
            StatusInterp("Regen", Player, Foe, -1) #GainRegen(Player, Foe, -1)

        if Player.Poison > 0: 
            StatusInterp("Poison", Player, Foe, -1) #GainPoison(Player, Foe, -1)

        if Player.Stun > 0: 
            StatusInterp("Stun", Player, Foe, -1) #Stun(-1, Foe, Player)

        if Player.Riptide > 0: 
            StatusInterp("Riptide", Player, Foe, -1) #GainRiptide(Player, Foe, -1)

        if Player.Acid > 0: 
            StatusInterp("Acid", Player, Foe, -1) #GainAcid(Player, Foe, -1)

        if Player.Purity > 0: 
            StatusInterp("Purity", Player, Foe, -1) #GainPurity(Player, Foe, -1)

    if Name == "CandiedNuts": #Gain 3 thorns, thorns do 2x
        Player.Thorns = Player.Thorns + 3

    if Name == "CherryCocktail":  #Deal 3 damage and restore 3 hp
        #for nn in range(1, Player.Bombtrigger):
        BombDamage(3, Player, Foe)
        Sanguine(Player, Foe, 3)

    if Name == "CombustibleLemon":  #Spend 1 speed to deal 2 bomb damage
        if Player.Speed > 0:
            GainSpeed(Player, Foe, -1)
            BombDamage(2, Player, Foe)

    if Name == "DeepseaWine":  #Give foe 1 riptide. Whenever a riptide triggers restore 3 hp
        if Phase == "Wounded":
            StatusInterp("Riptide", Foe, Player, 1)
        if Phase == "RiptideTriggers":
            HealingCalc(Player, Foe, 3)

    if Name == "ExplosiveFish": #Give foe 1 riptide and deal 2xfoe.riptide bombdamage
        StatusInterp("Riptide", Foe, Player, 1)
        #GainRiptide(Foe, Player, 1)
        BombDamage(2*Foe.Riptide, Player, Foe)

    if Name == "ExplosiveRoast": #Deal 1 damage 4 times
    #Might be other order
        for nn in range(0, 4):
            BombDamage(1, Player, Foe)
            # Foe.Powder = max(0, Foe.Powder - 1)
            # Foe.Powder = Foe.Powder + 3

    if Name == "GraniteCherry":  #If your hp is full, gain 2 armor and deal 2 damage 3 times
        if Player.CurrentHP == Player.MaxHP:
            for ll in range(0, 3):
                ArmorGain(Player, Foe, 2)
                BombDamage(2, Player, Foe)

    if Name == "HoneyCaviar": #Give foe 10 riptide
        StatusInterp("Riptide", Foe, Player, 10)
        #GainRiptide(Foe, Player, 10)

    if Name == "HoneydewMelon": #Give all your status effects to the foe
        if Player.Thorns > 0: 
            x = Player.Thorns
            StatusInterp("Thorns", Player, Foe, -x)
            StatusInterp("Thorns", Foe, Player, x)

        if Player.Freeze > 0: 
            x = Player.Freeze
            StatusInterp("Freeze", Player, Foe, -x)
            StatusInterp("Freeze", Foe, Player, x)

        if Player.Regen > 0: 
            x = Player.Regen
            StatusInterp("Regen", Player, Foe, -x)
            StatusInterp("Regen", Foe, Player, x)

        if Player.Poison > 0: 
            x = Player.Poison
            StatusInterp("Poison", Player, Foe, -x)
            StatusInterp("Poison", Foe, Player, x)

        if Player.Stun > 0: 
            x = Player.Stun
            StatusInterp("Stun", Player, Foe, -x)
            StatusInterp("Stun", Foe, Player,  x)
            
        if Player.Riptide > 0: 
            x = Player.Riptide
            StatusInterp("Riptide", Player, Foe, -x)
            StatusInterp("Riptide", Foe, Player, x)

        if Player.Acid > 0: 
            x = Player.Acid
            StatusInterp("Acid", Player, Foe, -x)
            StatusInterp("Acid", Foe, Player, x)

        if Player.Purity > 0: 
            x = Player.Purity
            StatusInterp("Purity", Player, Foe, -x)
            StatusInterp("Purity", Foe, Player, x)

    if Name == "HoneyglazedShroom":  #Give the foe 2 poison
        StatusInterp("Poison", Foe, Player, 2)
        #GainPoison(Foe, Player, 2)

    if Name == "HornedMelon":  #Decrease 2 random status effects by 1 and gain that many thorns
            [Status, Stacks1] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect
            [Status, Stacks2] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect
            if Stacks1 + Stacks2 > 0:
                StatusInterp("Thorns", Player, Foe, Stacks1 + Stacks2)
                #GainThorns(Player, Foe, Stacks1 + Stacks2)

    if Name == "LemonRoast":  #Gain 2 acid
        StatusInterp("Acid", Player, Foe, 2)
        #GainAcid(Player, Foe, 2)

    if Name == "LemonShark":  #Gain 1 acid
        if Phase == "BattleStart":
            StatusInterp("Acid", Player, Foe, 1)
        
        if Phase == "Exposed":
            if Player.Acid > 0:
                StatusInterp("Riptide", Foe, Player, Player.Acid)
        #GainAcid(Player, Foe, 1)
        #Player.Items = [word.replace("LemonShark", "LemonSharkE") for word in Player.Items]
        # replaced = False
        # for jj in range(0, len(Player.Items)):
        #     if not replaced and Player.Items[jj] == "LemonShark":
        #         Player.Items[jj] = "LemonSharkE"
        #         replaced = True

    # if Name == "LemonSharkE": #Give the foe riptide = your acid
    #     StatusInterp("Riptide", Foe, Player, Player.Acid)
    #     #GainRiptide(Foe, Player, Player.Acid)

    if Name == "LemonSyrup": #Double your speed
        GainSpeed(Player, Foe, Player.Speed)

    if Name == "LimestoneFruit":  #Gain 8 armor, if hp isnt full gain 2 acid
        ArmorGain(Player, Foe, 8)
        if Player.CurrenHP != Player.MaxHP:
            StatusInterp("Acid", Player, Foe, 2)
            #GainAcid(Player, Foe, 2)

    if Name == "MarbleMushroom":  #Gain 3 poison
        StatusInterp("Poison", Player, Foe, 3)
        #GainPoison(Player, Foe, 3)

    if Name == "MarbledStonefish":  #If you hp is full, gain 5 armor and give foe 1 riptide
        if Player.CurrentHP == Player.MaxHP:
            ArmorGain(Player, Foe, 5)
            StatusInterp("Riptide", Foe, Player, 1)
            #GainRiptide(Foe, Player, 1)

    if Name == "MelonBomb": #Decrease a random status effect by 1. I believe both effects currently should trigger 3 times with powder keg but only the damage does
        if Phase == "BattleStart" or "Exposed" or "Wounded":
            [Status, Stacks1] = Player.RandomStatus(Foe, -1) #This automagically changes a random self status effect
        if Phase == "LoseStatus": #Whenever a status effect is decreased, deal 1 damage to foe.
            BombDamage(1, Player, Foe)

    if Name == "MelonLemonade":  #Remove all your acid
        if Player.Acid > 0:
            StatusInterp("Acid", Player, Foe, -Player.Acid)
            #GainAcid(Player, Foe, -Player.Acid)

    if Name == "MelonWine":  #Decrease a random status by 1 and restore 3 hp
        if Phase == "BattleStart" or "Exposed" or "Wounded":
            [Status, Stacks] = Player.RandomStatus(Foe, -1)
            if Stacks > 0:
                HealingCalc(Player, Foe, 3)

    if Name == "MineralWater":  #If HP is full, decrease a random status by 2 and gain 5 armor
        if Player.MaxHP == Player.CurrentHP:
            [Status, Stacks] = Player.RandomStatus(Foe, -2)
            ArmorGain(Player, Foe, 5)

    if Name == "MushroomSoup": #Gain 1 poison and 1 regen
        StatusInterp("Poison", Player, Foe, 1)
        #GainPoison(Player, Foe, 1)
        StatusInterp("Regen", Player, Foe, 1)
        #GainRegen(Player, Foe, 1)

    if Name == "PetrifiedChestnut": #If hp is full, gain 6 thorns and 6 armor
        if Player.MaxHP == Player.CurrentHP:
            #GainThorns(Player, Foe, 6)
            StatusInterp("Thorns", Player, Foe, 6)
            #Player.Armor = Player.Armor + 6
            ArmorGain(Player, Foe, 6)

    if Name == "PoisonousDurian":  #Gain 1 poison and 1 thorns
        StatusInterp("Poison", Player, Foe, 1)
        #GainPoison(Player, Foe, 1)
        StatusInterp("Thorns", Player, Foe, 1)
        #GainThorns(Player, Foe, 1)

    if Name == "PoisonousLemon": #Gain 1 acid and 5 poison
        StatusInterp("Acid", Player, Foe, 1)
        #GainAcid(Player, Foe, 1)
        StatusInterp("Poison", Player, Foe, 5)
        #GainPoison(Player, Foe, 5)

    if Name == "PoisonousPufferfish": #Gain 3 poison and give foe 2 riptide
        StatusInterp("Poison", Player, Foe, 3)
        #GainPoison(Player, Foe, 3)
        StatusInterp("Riptide", Foe, Player, 2)
        #GainRiptide(Foe, Player, 2)

    if Name == "PowderCookie":  #Gain 3 thorns and give foe 3 powder
        StatusInterp("Thorns", Player, Foe, 3)
        #GainThorns(Player, Foe, 3)
        Foe.Powder = Foe.Powder + 3

    if Name == "RoastedChestnut": #Gain 4 thorns
        StatusInterp("Thorns", Player, Foe, 4)
        #GainThorns(Player, Foe, 4) 

    if Name == "RockCandy": #Gain 15 armor, if hp is full gain 15 more. I think its individual
        ArmorGain(Player, Foe, 15)
        if Player.CurrentHP == Player.MaxHP:
            ArmorGain(Player, Foe, 15)

    if Name == "SharkRoast":  #Give foe 2 riptide
        StatusInterp("Riptide", Foe, Player, 2)
        #GainRiptide(Foe, Player, 2)

    if Name == "SpikedWine": #Gain 5 thorns and restore 5 hp
        StatusInterp("Thorns", Player, Foe, 5)
        #GainThorns(Player, Foe, 5)
        HealingCalc(Player, Foe, 5)

    if Name == "SpinyKiwifruit":  #Gain 3 acid and gain thorns = acid
        StatusInterp("Acid", Player, Foe, 3)
        #GainAcid(Player, Foe, 3)
        if Player.Acid > 0:
            StatusInterp("Thorns", Player, Foe, Player.Acid)
            #GainThorns(Player, Foe, Player.Acid)

    if Name == "SpinySnapper":  #Give foe 1 riptide. Whenever riptide triggers, gain 3 thorns
        if Phase == "BattleStart":
            StatusInterp("Riptide", Foe, Player, 1)
        if Phase == "RiptideTriggers":
            StatusInterp("Thorns", Player, Foe, 3)

    if Name == "SugarBomb":  #Deal 1 damage 3 times
        for nn in range(0, 3):
            BombDamage(1, Player, Foe)
            # Foe.Powder = max(0, Foe.Powder - 1)

    if Name == "SweetWine":
        HealingCalc(Player, Foe, 30)

    if Name == "ToxicCherry":  #Gain 1  poison and deal 1 damage to foe
        StatusInterp("Poison", Player, Foe, 1)
        #GainPoison(Player, Foe, 1)
        BombDamage(1, Player, Foe)

    if Name == "TrailMix":  #Deal 1 damage and gain 1 thorn 3 times
        for ll in range(0, 3):
            BombDamage(1, Player, Foe)
            StatusInterp("Thorns", Player, Foe, 1)
            #GainThorns(Player, Foe, 1)

    if Name == "UnderwaterWatermelon":  #Decrease 1 random status effect and give foe 1 riptide
        [Status, Stacks] = Player.RandomStatus(Foe, -1)
        StatusInterp("Riptide", Foe, Player, 1)

    if Name == "EchoRune":  #Wounded: Retrigger a random batstart item
        Player.RandomSearch("BattleStart", Foe)

    if Name == "BeltOfGluttony":  #Just Stats*
        Player.Armor = Player.Armor

    if Name == "BootsOfSloth":  #Just Stats*
        Player.Armor = Player.Armor
    
    if Name == "ChestOfLust":  #Just Stats*
        Player.Armor = Player.Armor
    
    if Name == "HelmetOfEny": #Double foe's Attack
        Foe.Attack = 2*Foe.Attack

    if Name == "BattleAxe":  #Deal 2x if foe is armored. Maybe add "Strike" tag
        if Foe.Armor > 0:
            Player.StrikeMult = 2*Player.StrikeMult

    if Name == "BoomStick": # On hit deal one damage
        #for nn in range(1, Player.Bombtrigger): #might retrigger strikes????
        BombDamage(1, Player, Foe)
        #Foe.Powder = max(0, Foe.Powder - 1)

    if Name == "BrittlebarkBow": # After 3 strikes: lose 2 attack p sure triggers once
        if Player.StrikeCounter == 3:
            Player.Attack = Player.Attack - 2
        #Player.StrikeCounter = Player.StrikeCounter + 1
            
    # if Name == "ElderwoodStaff":  #Its just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    # if Name == "FeatherweightBlade":  #Its just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    if Name == "ForgeHammer":  #Give the enemy 2 armor
        #This *might* give the armor at the wrong time
        #Foe.Armor = Foe.Armor + 2
        ArmorGain(Foe, Player, 2)

    if Name == "FungalRapier":  #Gain 1 Poison
        StatusInterp("Poison", Player, Foe, 1)
        #GainPoison(Player, Foe, 1)

    if Name == "GaleStaff":  #Lose 1 Speed
        GainSpeed(Player, Foe, -1)

    if Name == "GrillingSkewer":  #Gain 1 additional strike(temp)
        Player.StrikesCount = Player.StrikesCount + 1

    if Name == "Haymaker":  # Every 3 strikes gain another one
        if Player.StrikeCounter % 3 == 2:
            GainStrikes(Player, Foe, 1)

    if Name == "HeartDrinker": #On Hit: Restore 1 hp
        Sanguine(Player, Foe, 1)

    # if Name == "HiddenDagger": #It gives more attack the more HD you have, aka just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    # if Name == "IronstoneGreatsword": #Just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    if Name == "IronstoneSpear":  #While you have armor, temp gain 2 attack
        if Player.Armor > 0:
            Player.TempAttack = Player.TempAttack + 2

    if Name == "LiferootStaff":  #Gain 3 regen when wounded
        StatusInterp("Regen", Player, Foe, 3)
        #GainRegen(Player, Foe, 3)

    if Name == "MarbleSword":  #Exposed: Gain 3 attack
        Player.Attack = Player.Attack + 3

    if Name == "PacifistStaff":  #Gain 1 armor and restore 1 hp
        #Player.Armor = Player.Armor + 1
        ArmorGain(Player, Foe, 1)
        HealingCalc(Player, Foe, 1)

    if Name == "RazorthornSpear":  #Gain 2 thorns on hit
        StatusInterp("Thorns", Player, Foe, 2)
        #GainThorns(Player, Foe, 2)
    
    # if Name == "RedwoodRod": #It gives more attack the more HD you have, aka just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    if Name == "SilverscaleDagger": #Give 1 Riptide
        StatusInterp("Riptide", Foe, Player, 1)
        #GainRiptide(Foe, Player, 1)

    if Name == "SlimeSword": #Give yourself and the foe 3 acid
        StatusInterp("Acid", Player, Foe, 3)
        StatusInterp("Acid", Foe, Player, 3)
        #GainAcid(Player, Foe, 3)
        #GainAcid(Foe, Player, 3)

    # if Name == "SpearshieldLance": #It gives more attack the more HD you have, aka just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    if Name == "StormcloudSpear": #Every 5 Strikes, stun the enemy for 2 turns. when its divisible by 5.
        if Player.StrikesCounter%5 == 0:
            StatusInterp("Stun", Foe, Player, 2)
            #Stun(2, Player, Foe)

    # if Name == "SwordOfTheHero": #It gives more attack the more HD you have, aka just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    # if Name == "WoodcuttersAxe": #It gives more attack the more HD you have, aka just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    # if Name == "WoodenStick": #It gives more attack the more HD you have, aka just stats
    #     #Stats Only Weapon does nothing
    #     Player.Attack = Player.Attack

    if Name == "ArcaneWand": #Cant Attack. TS: Deal 2 + Count(Tome) damage
        DealDamage(2 + Count(Player, "Tome"), Player, Foe)

    if Name == "BasiliskFang": #Decrease self poison by 2 and give it to foe.
        if Player.Poison > 0:
            x = min(2, Player.Poison)
            StatusInterp("Poison", Player, Foe, -x)
            StatusInterp("Poison", Foe, Player, x)

    if Name == "BejeweledBlade":  # Gains 2 attack per jewelry item in inv
        c = Count(Player, "Jewelry")
        Player.Attack = Player.Attack + 2*c #Maybe this should be a base stats thing

    if Name == "BlackbriarBlade":  #Gain 2 attack per thorn you have
        Player.TempAttack = Player.TempAttack + 2*Player.Thorns

    if Name == "BloodmoonDagger": # Gain 5 attack and take 2 self damage
        Player.Attack = Player.Attack + 5
        SelfArmorLose(Player, Foe, 2)

    if Name == "BloodmoonSickle": # 1 Self damage
        SelfArmorLose(Player, Foe, 1)

    if Name == "BubblegloopStaff": #Spend 1 speed to give the foe 1 acid and 2 poison
        if Player.Speed > 0:
            GainSpeed(Player, Foe, -1)
            StatusInterp("Acid", Foe, Player, 1)
            #GainAcid(Foe, Player, 1)
            #GainPoison(Foe, Player, 2)
            StatusInterp("Poison", Foe, Player, 2)

    if Name == "ExplosiveSword":  #Whenever a bomb does 5 or more explosive damage, gain 1 additional strike
        GainStrikes(Player, Foe, 1)

    # if Name == "ExplosiveSword": #Deal 3 damage (Bomb)
    #     Player.Attack = Player.Attack
    #     # for nn in range(1, Player.Bombtrigger):
    #     #     DealDamage(3 + Foe.Powder, Player, Foe)
    #     #     Foe.Powder = max(0, Foe.Powder - 1)

    if Name == "FrostbiteDagger": #Give the foe freeze = your attack on hit
        Player.FreezeMult = 1
        if Player.Freeze > 0:
            Player.FreezeMult = 0.5
        StrikeMult(Player, Foe)
        if np.floor((Player.StrikeMult*(Player.Attack + Player.TempAttack))*Player.FreezeMult) > 0:
            StatusInterp("Freeze", Foe, Player, np.floor((Player.StrikeMult*(Player.Attack + Player.TempAttack))*Player.FreezeMult))
            #Freeze(np.floor((Player.StrikeMult*(Player.Attack + Player.TempAttack))*FreezeMult), Player, Foe)
        Player.StrikeMult = 1

    if Name == "GraniteAxe":  #Lose 3 hp and gain 3 armor
        Player.CurrentHP = Player.CurrentHP - 3
        HP1Check(Player, Foe)
        #Player.Armor = Player.Armor + 3
        ArmorGain(Player, Foe, 3)
        TakeDamage(Player, Foe)

    if Name == "IcicleSpear": #Give the enemy 1 freeze for each equipped water item
        StatusInterp("Freeze", Foe, Player, Count(Player, "Water"))
        #Freeze(Count(Player, "Water"), Player, Foe)

    if Name == "IronstoneBow":  #On hit lose 1 speed. If Speed is 0 or less only attack every other turn
        Player.Speed = Player.Speed - 1

    #if Name == "LifebloodSpear" : {"Weapon", "FirstHPRestore"}, #Gains attack = first hp restored sounds hard

    if Name == "LightningRod":  #If stunned, gain 1 attack
        if Player.Stun > 0:
            Player.Attack = Player.Attack + 1

    if Name == "LightningWhip":  #If foe is stunned, gain 1 strike
        if Foe.Stun > 0:
            Player.StrikesCount = Player.StrikesCount + 1

    if Name == "RingBlades": #Steal 1 attack from foe
        if Foe.Attack > 0:
            Foe.Attack = Foe.Attack - 1
            Player.Attack = Player.Attack + 1

    if Name == "RustySword":  #If the foe has no armor deal additional damage equal to foe acid
        if Foe.Armor == 0:
            DealDamage(Foe.Acid, Player, Foe)

    #if Name == "SanguineScepter": #Healing doubled

    if Name == "SwiftstrikeRapier": #If you have more speed than foe, gain 2 strikes
        GainStrikes(Player, Foe, 2)

    if Name == "WaveBreaker":  #Give the foe 2*(negative base attack) riptide
        if Player.Attack < 0:
            StatusInterp("Riptide", Foe, Player, 2*(-Player.Attack))
            #GainRiptide(Foe, Player, 2*(-Player.Attack))

    if Name == "BloodlordsAxe":  #Foe loses 5 hp, you restore 5 hp
        Foe.CurrentHP = Foe.CurrentHP - 5
        HP1Check(Foe, Player)
        TakeDamage(Foe, Player)
        Sanguine(Player, Foe, 5)

    if Name == "BrittlebarkClub": #Exp or Wound lose 2 attack
        if Player.NoBBB:
            Player.Attack = Player.Attack - 2

    if Name == "ChainmailSword":  #Gain armor equal to base armor
        ArmorGain(Player, Foe, Player.BaseArmor)

    if Name == "FrozenIceblade":  #Gain 3 freeze
        StatusInterp("Freeze", Player, Foe, 3)
        #Freeze(3, Foe, Player)

    if Name == "GemstoneScepter": #Gain an on hit effect if you have emerald(+1HP), ruby(+1damage), sapphire(+1Armor), or citrine(+1spd) items
        #Might need it to check for all jewelry types simitaneously
        for i in range(0, Count(Player, "Emerald")):
            HealingCalc(Player, Foe, 1)
        
        for i in range(0, Count(Player, "Ruby")):
            DealDamage(1, Player, Foe)
        
        for i in range(0, Count(Player, "Sapphire")):
            #Player.Armor = Player.Armor + 1
            ArmorGain(Player, Foe, 1)

        for i in range(0, Count(Player, "Citrine")):
            #Player.Speed = Player.Speed + 1
            Player.DeltaSpeed = 1
            GainSpeed(Player, Foe, 1)

    if Name == "GraniteHammer": #Convert 1 armor to 2 attack p sure this the right order to gain the attack
        if Player.Armor > 0:
            SelfArmorLose(Player, Foe, 1)
            Player.Attack = Player.Attack + 2

    # if Name == "GraniteLance" : {"Weapon", "Stone"}, #Stat effect 2x base armor
    #     #base stats

    # if Name == "GrindstoneClub" : {"Weapon", "Stone"}, #Effect +2 attack to next weapon equipped (Makes figuring out weapon base stats more annoying)
    #     #Base stats

    if Name == "KingsBlade":  #Wounded and Exposed trigger at battle start
        Player.WoundTriggers = Player.WoundTriggers - 1
        Player.ExposedTriggers = Player.ExposedTriggers - 1
        if "BloodChain" in Foe.Items:
            Player.MultiSearch("Wounded" or "Exposed", Foe, "Wounded" or "FoeExposed") #It might activate all the faster persons items first instead of a slot by slot check
        else:
            Player.MultiSearch("Wounded" or "Exposed", Foe, "FoeExposed")

    if Name == "LeatherWhip":  #Gain 5 max hp
        #Might need to add a check for honey roast
        Player.MaxHP = Player.MaxHP + 5
        Player.Wounded(Foe)

    if Name == "LifestealScythe": #Restore HP = Damage done to HP
        Sanguine(Player, Foe, Foe.HPloseFromFoeStrike)

    if Name == "MeltingIceblade":  #Lose 1 attack
        Player.Attack = Player.Attack - 1 #Maybe need to not do this with the HolyCrucifix itemset

    if Name == "MoonlightCleaver":  #If below 50% hp cannot gain status
        if Player.CurrenHP/Player.MaxHP < 0.5:
            Player.PreventStatusGain = True

    if Name == "PurelakeStaff":  #BS: Gain 2 purity. OH: Lose 1 purity
        StatusInterp("Purity", Player, Foe, 2)
        #GainPurity(Player, Foe, 2)
        Player.Items = [word.replace("PurelakeStaff", "PurelakeStaffOH") for word in Player.Items]

    if Name == "PurelakeStaffOH":  #BS: Gain 2 purity. OH: Lose 1 purity
        if Player.Purity > 0:
            StatusInterp("Purity", Player, Foe, -1)
            #GainPurity(Player, Foe, -1)

    if Name == "QuickgrowthSpear":  #Gain 1 attack and restore 1 HP
        Player.Attack = Player.Attack + 1
        HealingCalc(Player, Foe, 1)

    if Name == "RiverflowRapier":  #First time you gain a new status effect, gain 1 strike
        GainStrikes(Player, Foe, 1)

    if Name == "RoyalCrownblade":  #Gain 1 Gold
        Player.Gold = Player.Gold + 1
         
    if Name == "RoyalScepter":  #Sets attack always equal to gold. Cannot have more than 10 gold
        Player.TempAttack = 0
        Player.FreezeMult = 1
        Player.Gold = min(10, Player.Gold)
        Player.Attack = Player.Gold

    if Name == "SerpentDagger": #Every 3 strikes give the foe 4 poison
        if Player.StrikeCounter%3 == 0:
            StatusInterp("Poison", Foe, Player, 4)
            #GainPoison(Foe, Player, 4)
        
    if Name == "SilverscaleTrident":  #Give 1 riptide
        StatusInterp("Riptide", Foe, Player, 1)
        #GainRiptide(Foe, Player, 1)

    if Name == "StoneslabSword":  #Gain 2 armor
        #Player.Armor = Player.Armor + 2
        ArmorGain(Player, Foe, 2)

    if Name == "ThunderboundSabre":  #Stun yourself for 2 turns
        StatusInterp("Stun", Player, Foe, 2)
        #Stun(2, Foe, Player)

    if Name == "TwinBlade":  #Base strikes count = 2
        Player.BaseStrikesCount = 2

    if Name == "BearclawBlade":  #Attack = Missing HP
        Player.TempAttack = 0
        Player.FreezeMult = 1
        Player.Attack = max(0, Player.MaxHP  - Player.CurrentHP) #Shouldnt need max/min aslong as hps work correctly

    if Name == "MountainCleaver":  #Attack = Base Armor
        Player.Attack = Player.BaseArmor
    
    if Name == "TempestBlade": #Attack = Speed
        Player.TempAttack = 0
        Player.FreezeMult = 1
        Player.Attack = max(0, Player.Speed)

    if Name == "SwordOfPride":  #If the foe has more attack, armor, or speed, take 3 damage
        if Player.Attack < Foe.Attack:
            SelfArmorLose(Player, Foe, 3)
        if Player.Armor < Foe.Armor:
            SelfArmorLose(Player, Foe, 3)
        if Player.Speed < Foe.Speed:
            SelfArmorLose(Player, Foe, 3)

    if Name == "BlackbriarBow":  #Turn Start gain thorns = to your attack
        StatusInterp("Thorns", Player, Foe, Player.Attack)

    if Name == "CherryBlade":  #Deal 4 damage on batstart and exposed
        BombDamage(4, Player, Foe)

    if Name == "DeathcapBow": #BS: Gain 3 Poison. TS: Gain 1 additional strike, if you are poisoned
        if Phase == "BattleStart":
            StatusInterp("Poison", Player, Foe, 3)

        if Phase == "TurnStart":
            if Player.Poison > 0:
                GainStrikes(Player, Foe, 1)

    if Name == "HamBat":  #Gain 2 additional strikes
        GainStrikes(Player, Foe, 2)

    if Name == "LemontreeBranch": #{"Weapon", "OnHit", "Food", "Wood"}, #Spend 2 speed to gain an additional strike
        if Player.Speed > 1:
            GainSpeed(Player, Foe, -2)
            GainStrikes(Player, Foe, 1)

    if Name == "MelonvineWhip":  #On hit remove 1 stack of a random status effect on self
        Player.RandomStatus(Foe, -1)

    if Name == "RocksaltSword":  #if your hp is full, gain 1 additional strike
        if Player.CurrentHP == Player.MaxHP:
            GainStrikes(Player, Foe, 1)

    if Name == "SilverscaleSwordfish":  #Gain 1 extra strike on battle start, #First Turn on hit give the foe 1 riptide
        if Phase == "BattleStart":
            GainStrikes(Player, Foe, 1)
        if Phase == "FirstTurn":
            StatusInterp("Riptide", Foe, Player, 1)

    #Blacksmith Edge
    if Name == "AgileEdge": #Gain 1 additional strike on first turn
        GainStrikes(Player, Foe, 1)
    
    if Name == "BleedingEdge": #Restore 1 HP
        HealingCalc(Player, Foe, 1)

    if Name == "BluntEdge": #Gain 1 armor
        #Player.Armor = Player.Armor + 1
        ArmorGain(Player, Foe, 1)

    if Name == "CleansingEdge":  #Ignore the first Status effect you are afflicted with
        if Player.FirstStatus:
            Player.PreventStatusGain = True
            Player.FirstStatus = False

    if Name == "CuttingEdge":  #Deal 1 Damage
        DealDamage(1, Player, Foe)

    if Name == "FeatherweightEdge":  #Convert 1 Speed to 1 Attack
        if Player.Speed > 0:
            #Player.Speed = Player.Speed - 1
            GainSpeed(Player, Foe, -1)
            Player.Attack = Player.Attack + 1

    if Name == "FreezingEdge": #Give foe 3 freeze
        StatusInterp("Freeze", Foe, Player, 3)
        #Freeze(3, Player, Foe)

    if Name == "GildedEdge": #If Gold < 10, Gain 1 gold
        if Player.Gold < 10:
            Player.Gold = Player.Gold + 1

    if Name == "JaggedEdge": #Gain 2 thorns and take 1 self damage
        StatusInterp("Thorns", Player, Foe, 2)
        #GainThorns(Player, Foe, 2)
        SelfArmorLose(Player, Foe, 1)

    if Name == "OakenEdge":  #Gain 3 regen
        StatusInterp("Regen", Player, Foe, 3)
        #GainRegen(Player, Foe, 3)

    if Name == "OozingEdge":  #If foe poison = 0, give 2 poison
        if Foe.Poison == 0:
            StatusInterp("Poison", Foe, Player, 2)
            #GainPoison(Foe, Player, 2)

    if Name == "PetrifiedEdge":  #Double your attack, OH: gain 1 stun
        StatusInterp("Stun", Player, Foe, 1)
        #Stun(1, Foe, Player)

    if Name == "PlatedEdge":  #Convert 1 speed to 3 armor
        if Player.Speed > 0:
            GainSpeed(Player, Foe, -1)
            ArmorGain(Player, Foe, 3)

    if Name == "RazorEdge":  #Gain 1 attack
        Player.Attack = Player.Attack + 1

    if Name == "SmokingEdge": #Give 1 powder to foe
        Foe.Powder = Foe.Powder + 1

    if Name == "StormcloudEdge": #Stun foe for 1 turn
        StatusInterp("Stun", Foe, Player, 1)
        #Stun(1, Player, Foe)

    if Name == "WhirlpoolEdge":  #Every 3 strikes, give 1 riptide
        if Player.StrikeCounter%3 == 0:
            StatusInterp("Riptide", Foe, Player, 1)
            #GainRiptide(Foe, Player, 1)

    if Name == "BloodmoonStrike": ##On your next turn restore hp = to damage done by strikes(I am assuming is would have the right order)
        HealingCalc(Player, Foe, Foe.DamageFromFoeStrike)

    if Name == "BriarGreaves": #On take damage, gain 1 thorn
        StatusInterp("Thorns", Player, Foe, 1)
        #GainThorns(Player, Foe, 1)

    if Name == "ElderwoodMask":  #Double all base attack, armor, speed
        #This sound work in most cases
        Player.Attack = 2*Player.Attack
        Player.Armor = 2*Player.Armor
        Player.Speed = 2*Player.Speed

    if Name == "IronbarkShield": #If HP = max HP at BatStart then gain IronbarkShieldTS item
        if Player.MaxHP == Player.CurrentHP:
            Player.Items = [word.replace("IronbarkShield", "IronbarkShieldTS") for word in Player.Items]

    if Name == "IronbarkShieldTS": #1 Armor Gain at turn start 
        ArmorGain(Player, Foe, 1) 

    if Name == "LifebloodTransfusion":  #Restore 10 HP after battle.
        x = 10
        if Player.CurrentHP/Player.MaxHP:
            x = x*Player.TwilightCrestMult
        if Player.Stun > 0:
            x = x*Player.VampireCloak
        Player.CurrentHP = min(Player.MaxHP, Player.CurrentHP + x*Player.SanguineScepterMult) #I dont think this activates the other effects

    if Name == "RawHide":  #Gain 1 attack
        Player.Attack = Player.Attack + 1

    if Name == "RedwoodCrown": #Restore HP to Full
        HealingCalc(Player, Foe, Player.MaxHP - Player.CurrentHP)

    if Name == "SaffronTalon": #Gain +1 Speed on hit
        #Player.Speed = Player.Speed + 1
        Player.DeltaSpeed = 1
        GainSpeed(Player, Foe, 1)

    if Name == "SteelplatedThorns": #Whenever you lose thorns gain that much armor
        if Player.Thorns > 0:
            #Player.Armor = Player.Armor + Player.Thorns
            ArmorGain(Player, Foe, Player.ThornsDecrease)

    if Name == "BasilisksGaze":  #Your foe is stunned for 2 turns
        StatusInterp("Stun", Foe, Player, 2)
        #Stun(2, Player, Foe)

    if Name == "DeadlyToxin":  #First time foe gains poison, give 2 acid
        if Player.DeadlyToxin:
            Player.DeadlyToxin = False
            StatusInterp("Acid", Foe, Player, 2)
            #GainAcid(Foe, Player, 2)

    if Name == "IronstoneCrest":  #Steal 2 armor from foe
        if Foe.Armor > 0:
            ArmorGain(Player, Foe, min(2, Foe.Armor))
            ArmorLose(Foe, Player, min(2, Foe.Armor))

    if Name == "IronstoneFang":  #Gain 3 armor on hit
        ArmorGain(Player, Foe, 3)

    if Name == "MarbleAnvil":  #Exposed trigger at battle start
        Player.ExposedTriggers = Player.ExposedTriggers - 1
        Player.MultiSearch("Exposed", Foe, "FoeExposed")

    if Name == "MarshlightAria": #When exposed: Trigger symphony twice
        for pp in range(0, 2):
            Symphony(Player, Foe, "")

    if Name == "SeafoodHotpot": #Gain 2 armor per speed
        ArmorGain(Player, Foe, 2*Player.Speed)

    if Name == "WeaverMedallion": #Spend 1 armor to gain 1 attack
        if Player.Armor > 0:
            SelfArmorLose(Player, Foe, 1)
            Player.Attack = Player.Attack + 1

    if Name == "IronstoneArrowhead": #Gain 1 armor on hit
        ArmorGain(Player, Foe, 1)

    if Name == "IronstoneOre": #Gain armor = negative speed
        if Player.Speed < 0:
            ArmorGain(Player, Foe, -Player.Speed)

    if Name == "SanguineGemstone": #If your attack == 1, restore 1 hp on hit? Idk if its sanguine
        if Player.Attack == 1:
            HealingCalc(Player, Foe, 1)

    #Enemy effects
    if Name == "Bat": #Heal 1+Lvl HP OnHit every other strike: Lvl is Level - 1
        HealingCalc(Player, Foe, Player.Level)

    if Name == "Bear": #Gains 3+Lvl attack if foe has armor
        if Foe.Armor > 0:
            Player.TempAttack = Player.TempAttack + 2 + Player.Level 

    if Name == "Hedgehog": #Gains 3+Lvl thorns on BattleStart
        StatusInterp("Thorns", Player, Foe, 2 + Player.Level)
        #GainThorns(Player, Foe, 2 + Player.Level)

    if Name == "Raven": # OnHit steals 1+Lvl gold
        if Foe.Gold > Player.Level:
            Player.Gold = Player.Gold + Player.Level
            Foe.Gold = Foe.Gold - Player.Level
        else:
            Player.Gold = Player.Gold + Foe.Gold
            Foe.Gold = 0

    if Name == "Spider": #If Spider is faster, then it deals 3+Lvl damage BattleStart
        if Player.Speed > Foe.Speed:
            DealDamage(2+Player.Level, Player, Foe)

    if Name == "Wolf":  #If Foe.CurrenHP <=5 temp attack is set to +2+Lvl
        if Foe.CurrentHP <= 5:
            Player.TempAttack = Player.TempAttack + 1 + Player.Level

    #Night 1 Bosses
    if Name == "BlackKnight": # Gain attack = Foe.Attack + 2 Might be prebattle but p sure its a battlestart speed, might be slower tho
        Player.Attack = Player.Attack + Foe.Attack + 2

    if Name == "BloodmoonWerewolf":  #When player is below 50% HP, gains 5 attack
        if Foe.CurrentHP/Foe.MaxHP < 0.5:
            Player.TempAttack = Player.TempAttack + 5

    if Name == "BrittlebarkBeast": #Whenever you take damage take 3 more
        SelfArmorLose(Player, Foe, 3)

    if Name == "IronstoneGolem": #When exposed lose 3 attack
        Player.Attack = Player.Attack - 3

    #if Name == "RazorclawGrizzly":  #Attacks ignore armor

    if Name == "RazortuskHog": #If Razortusk Hog has more speed, first strike does 10 extra damage
        if Player.Speed > Foe.Speed: #Check might be on battlestart?
            Player.TempAttack = Player.TempAttack + 10

    #if Name == "MountainTroll": #Only strikes every other turn

    if Name == "BlackbriarKing": #CANNOT ATTACK, instead gains 2 thorns every turn. 4 if wounded(Below 50% hp)
        if Player.CurrentHP/Player.MaxHP > 0.5:
            StatusInterp("Thorns", Player, Foe, 2)
            #GainThorns(Player, Foe, 2)
        else:
            StatusInterp("Thorns", Player, Foe, 4)
            #GainThorns(Player, Foe, 4)
    
    if Name == "SwiftstrikeStag":  #Strikes 3 times
        Player.BaseStrikesCount = 3

    #if Name == "Leshen": #Currently does nothing

    if Name == "WoodlandAbomination":  #Gain an attack
        Player.Attack = Player.Attack + 1

    if Name == "IronshellBeetle":  #Lose 1 attack on hit (Up to 0)
        if Player.Attack > 0:
            Player.Attack = Player.Attack - 1

    if Name == "SilkweaverQueen":  #Turn Start steals 1 speed. If the foe has 0 or less speed, deal 3 damage instead
        if Foe.Speed > 0:
            Foe.Speed = Foe.Speed - 1
        elif 0 >= Foe.Speed:
            DealDamage(3, Player, Foe)

    return [Player, Foe]

def Healable(Player):
    x = False
    if Player.MaxHP - Player.CurrentHP > 0:
        x = True
    return x

def HPRestored(Player, Foe):
    Player.Search("HPRestored", Foe)

def HPOverHeal(Player, Foe):
    Player.Search("HPOverHeal", Foe)

def Sanguine(Player, Foe, Value):
    HealingCalc(Player, Foe, Player.SanguineMult*Value)

def HealingCalc(Player, Foe, Value):
    if Player.CurrentHP/Player.MaxHP < 0.5:
        Value = Player.TwilightCrestMult*Value
    if Player.Stun > 0:
        Value = Value*Player.VampireCloak    
    Value = Value*Player.SanguineScepterMult
    x = Player.CurrentHP - Player.MaxHP + Value
    if Healable(Player):
        Player.CurrentHP = min(Player.MaxHP, Player.CurrentHP + Value)
        if Player.FirstHealToggle == True:
            FirstHPRestore(Player, Foe, min(Value, Value - x))
        HPRestored(Player, Foe)
    if "HPOverHeal" in Player.Items and x > 0:
        DealDamage(x, Player, Foe)

def ArmorGain(Player, Foe, NewArmor):
    if NewArmor > 0:
        Player.GainedArmor = True
        if Player.PlatedShield:
            NewArmor = 2*NewArmor
            Player.PlatedShield = False
        Player.Armor = Player.Armor + NewArmor
        Player.Search("ArmorGain", Foe)

def GainStrikes(Player, Foe, Value):
    mult = 1
    if "SwiftstrikeBow" in Player.Items: #Can generalize if more gain strikes are added
        mult = 2
    Player.StrikesCount = Player.StrikesCount + mult*Value

def TakeDamage(Player, Foe): 
    Player.Wounded(Foe) #Might need to run all three at the same time
    Player.Exposed(Foe)
    Player.Search("TakeDamage", Foe)

def OnHit(Player, Foe):
    if Player.FirstTurn:
        Player.Search("OnHit" or "FirstTurnOnHit", Foe)
    else:
        Player.Search("OnHit", Foe)


def GainSpeed(Player, Foe, SpeedChange):
    if SpeedChange > 0:
        Player.Speed = Player.Speed + SpeedChange
        Player.Search("GainSpeed", Foe)
        Player.DeltaSpeed = 0
    else:
        Player.Speed = Player.Speed + SpeedChange
        Player.Search("LoseSpeed", Foe)
        Player.DeltaSpeed = 0

def GainThorns(Player, Foe, Value):
    if Value > 0:
        if "SpikyClub" in Player.Items:
            Player.Attack = Player.Attack + Value
        else:
            Player.Thorns = Player.Thorns + Value
            Player.Search("GainThorns", Foe)
    elif Value < 0:
        ThornsLose(Player, Foe, Value)

def ThornsLose(Player, Foe, Value):
    Player.Thorns = Player.Thorns + Value
    Player.ThornsDecrease = -Value
    Player.Search("ThornsLose", Foe)
    Player.ThornsDecrease = 0
    Player.FirstThornLose = False


def ArmorLose(Player, Foe): #This needs the Deltaarmor value for razorscales and sapphire gemstone
    Player.Search("ArmorLose", Foe)
    Player.DeltaArmor = 0 #I think thats the right spot

def Nonweapon(Player, Foe):
    Player.Search("Nonweapon", Foe)


def Count(Player, Tag):
    c = Player.Count(Tag)
    return c

def Symphony(Player, Foe, Instrument):
    #I think I can use the new "Phase" system to make it so I only need 1 instrument item and include the "Symphony" Phase tag to not trigger another symphony unless you have the one item.
    #Triggers a random instrument(Not the one that was triggered)
    List = []
    for slot in range(0, len(Player.Items)): #max(len(P.Items), len(Foe.Items))):
        if "Instrument" in ItemTags[Player.Items[slot]]:
            List = List.append(slot)
    List.remove(Instrument)
    #This *probably* works Idk
    if List != []:
        RanNumber = random.randint(0, len(List))
        slot = int(List(RanNumber))
        Choice = Player.Items[slot].append("S")
        [Player, Foe] = ItemsEffect("Symphony", "".join(Choice), Player, Foe)

def TurnCount(Player, Foe, TurnNum):
    Player.TurnCounter = Player.TurnCounter + 1
    #I think CD go first before turnstart? *Might* be end of turn
    Player.Cooldown = Player.Cooldown + 1
    Player.Search("Cooldown", Foe)

    if TurnNum == 0:
        Player.Search("TurnStart" or "EveryOtherTurn" or "FirstTurn", Foe)

    elif TurnNum % 2 == 0:
        Player.Search("TurnStart" or "EveryOtherTurn", Foe)

    else:
        Player.Search("TurnStart" or "OddEveryOtherTurn", Foe)

    if Player.Armor > 0 and Player.Acid > 0:
        Player.DeltaArmor = min(Player.Armor, Player.Acid)
        Foe.Search("AcidDamage", Player)

    if Player.Armor == 0 and Player.Poison > 0:
        DealDamage(Player.Poison, Foe, Player)
        StatusInterp("Poison", Player, Foe, -1)
        #GainPoison(Player, Foe, -1)

def FirstHPRestore(Player, Foe, Value):
    Player.FirstHealToggle = False
    for slot in range(0, len(Player.Items)): #max(len(P.Items), len(Foe.Items))):
        if "FirstHPRestore" in ItemTags[Player.Items[slot]]:
            Player.Attack = Player.Attack + Value

#Currently Only Ironstonesandals use this attribute could maybe make the crackedwhetstone use it too
def PreStrikeAttackBonus(Player, Foe):
    Player.Search("PreStrike", Foe)
    Foe.Search("PreFoeStrike", Player)

def PreStrikeL(Player, Foe):
    Player.TempAttack = 0
    Player.Search("PreStrikeL", Foe)

def AfterFoeFirstStrike(Player, Foe):
    Player.Search("AfterFoeFirstStrike", Foe)

#Checks if you have item that acts on selfarmor lose. And calcs the damage you take
#Hmmmmmmmmmmmmmmmmmmmmmmmmmm I think the sword talisman shouldnt be in the deal damage function?
def SelfArmorLose(Player, Foe, DamageValue):
    if "BloodmoonArmor" in Player.Items: #Can be more generalized
        DealDamage(DamageValue, Player, Foe)
    elif "SelfArmorLose" in ItemTags[Player.Items]:
        Player.CurrentHP = min(Player.CurrentHP, Player.CurrentHP + Player.Armor - DamageValue)
        HP1Check(Player, Foe)
        if Player.Armor > 0:
            Player.DeltaArmor = min(Player.Armor, DamageValue)
            ArmorLose(Player, Foe)
            ArmorGain(Player, Foe, Player.DeltaArmor)
            Player.DeltaArmor = 0
        TakeDamage(Player, Foe)
        #Idk why below was here removing it might break smth
    # else:
    #     #DealDamage(DamageValue, Foe, Player)
    #     if DamageValue > 0:
    #         Foe.CurrentHP = min(Foe.CurrentHP, Foe.CurrentHP + Foe.Armor - DamageValue) #Updates hp of foe if foe's armor reached 0
    #         HP1Check(Foe, Player)
    #         if Foe.Armor > 0:
    #             Foe.DeltaArmor = max(min(Foe.Armor, DamageValue), 0)
    #             ArmorLose(Foe, Player)
    #             Foe.DeltaArmor = 0
    #             Foe.Armor = max(0, Foe.Armor - DamageValue)
    #         TakeDamage(Foe, Player)

def StrikeMult(Player, Foe):
    Player.Search("StrikeMult", Foe)

def HP1Check(Player, Foe):
    if Player.CurrentHP < 5:
        Player.Search("HP5", Foe)
    if Player.CurrentHP == 1:
        Player.Search("HP1", Foe)

def EndBattleHeal(Player, Foe):
    Player.Search("BattleEnd", Foe)

def BombDamage(Damage, Player, Foe):
    #Add check to see if you do more damage/Retrigger
    for nn in range(0, Player.BombTrigger):
        DealDamage(Player.BombMult*(Damage + Player.BombBonus + Player.TempBombBonus), Player, Foe)
        if Player.BombMult*(Damage + Player.BombBonus + Player.TempBombBonus) >= 5:
            Player.Search("BombDamage5")

def SelfBombDamage(Damage, Player, Foe):
    #Add check to see if you do more damage/Retrigger
    for nn in range(0, Player.BombTrigger):
        DealDamage(Player.BombMult*(Damage + Player.BombBonus + Player.TempBombBonus), Foe, Player)
        if Player.BombMult*(Damage + Player.BombBonus + Player.TempBombBonus) >= 5:
            Player.Search("BombDamage5")

def GainFreeze(Player, Foe, FreezeCount):
    Player.Freeze = Player.Freeze + FreezeCount

def GainStun(Player, Foe, StunCount):
    Player.Stun = Player.Stun + StunCount

def GainPoison(Player, Foe, PoisonStacks):
    Player.Poison = Player.Poison + PoisonStacks
    #if PoisonStacks > 0:
    #StatusGain()
    #if PoisonStacks < 0:
    #StatusLose

def GainRiptide(Player, Foe, RiptideStacks):
    Player.Riptide = Player.Riptide + RiptideStacks
    #StatusGain()

def GainAcid(Player, Foe, AcidStacks):
    Player.Acid = Player.Acid + AcidStacks
    #StatusGain()

def GainRegen(Player, Foe, RegenStacks):
    Player.Regen = Player.Regen + RegenStacks
    #if RegenStacks > 0:
    #StatusGain()
    #if RegenStacks < 0:
    #StatusLose

def GainPurity(Player, Foe, PurityStacks):
    if PurityStacks > 0:
        Player.Purity = Player.Purity + PurityStacks
    elif Player.Purity >= -PurityStacks and PurityStacks < 0:
        Player.Purity = Player.Purity + PurityStacks
    elif Player.Purity < -PurityStacks and PurityStacks < 0:
        PurityStacks = -Player.Purity
        Player.Purity = 0
    #if PurityStacks > 0:
        #StatusGain()
    if PurityStacks < 0:
        Player.Attack = Player.Attack - PurityStacks
        HealingCalc(Player, Foe, -3*PurityStacks) #I think its 3*Purity lost. and not just 3 hp everytime its lost
    #StatusLose

def Cooldowned(Player, Foe):
    Player.Search("CooldownTrigger", Foe)

def EndTurn(Player, Foe, TurnNum):
    RipTriggs = Count(Player, "RiptideTriggers") + Count(Foe, "RiptideTriggers")
    if TurnNum == 0:
        Player.FirstTurn = False
        #Player.Search("FirstTurn", Foe) #Idk why this was here

    if Player.Freeze > 0:
        StatusInterp("Freeze", Player, Foe, -1)
        #Freeze(-1, Foe, Player)

    if Player.Regen > 0:
        if "GraniteQuill" in Player.Items:
            ArmorGain(Player, Foe, Player.Regen)
            StatusInterp("Regen", Player, Foe, -1)
            #GainRegen(Player, Foe, -1)
        else:
            HealingCalc(Player, Foe, Player.Regen)
            StatusInterp("Regen", Player, Foe, -1)
            #GainRegen(Player, Foe, -1)

    if Player.Stun > 0:
        StatusInterp("Stun", Player, Foe, -1)
        #Stun(-1, Foe, Player)

    if Player.Riptide > 0:
        if Player.FirstRiptide:
            Player.Search("FirstRiptide", Foe)
            Foe.Search("FirstRiptide", Player)
            Player.FirstRiptide = False
            Foe.FirstRiptide = False
        for nn in range(0, RipTriggs + 1):
            StatusInterp("Riptide", Player, Foe, -1)
            #GainRiptide(Player, Foe, -1)
            Player.Search("RiptideDamage", Foe)
            Foe.Search("RiptideDamage", Player)
            DealDamage(5, Foe, Player)

    Player.Search("EndTurn", Foe)
    #Also do other stuff like reduce freezecount activate turn end items

    
#Write a version without output and MAYBE check each time someone loses hp?
#Then have one at the end that displays the ending turns results
def checkLife(U1, U2, P): #Checks which player died and displays the values
    x = 0
    if U1.CurrentHP <= 0:
        #print("Player", P[0], "has died first")
        #print("Player", P[1], "has won:", U2.CurrentHP,"/", U2.MaxHP, "HP", U2.Armor, "Armor", U2.Attack, "Attack")
        x = 1
    if U2.CurrentHP <= 0:
        #print("Player", P[1], "has died first")
        #print("Player", P[0], "has won:", U1.CurrentHP,"/", U1.MaxHP, "HP", U1.Armor, "Armor", U1.Attack, "Attack")
        x = 1
    return x

#[10; 10; 3; 0; 4; SwordOfTheHero, CuttingEdge, ; 0; 0]
#[1; 1; 1; 0; 0; BluntEdge, HornedHelmet, HornedHelmet, HornedHelmet, VampireWine; 0; 0]


#Try making the input more intuitive? Maybe ask if its a player or enemy and then ask for stats for players and name for enemy?

# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print("Enter Stats for LEFT as follows(Need Weapon first, edge second, and then you can put more items)")
# print("[CurrentHp; MaxHp; Attack; Armor; Speed; Weapon, Item1, Item2; Level; Gold]: ")
# Left = input()
# Left = Left[1:-1].split('; ')

# for nn in range(0, 8):
#     if nn != 5:
#         Left[nn] = int(Left[nn])
#     else:
#         Left[nn] = Left[nn].split(", ")


# print("Player or Enemy?")
# Question = input()

# if Question == "Player":
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#     print("Enter Stats for RIGHT as follows(Need Weapon first, edge second, and then you can put more items)")
#     print("[CurrentHp; MaxHp; Attack; Armor; Speed; Weapon, Item1, Item2; Level; Gold]: ")
#     Right = input()
#     Right = Right[1:-1].split('; ')
#     for nn in range(0, 8):
#         if nn != 5:
#             Right[nn] = int(Right[nn])
#         else:
#             Right[nn] = Right[nn].split(", ")

# elif Question == "Enemy":
#     print("[EnemyName, Level]")
#     Enemy = input()
#     Enemy = Enemy[1:-1].split(', ')
#     Enemy[1] = int(Enemy[1])
#     Right = Enemies(Enemy[0], Enemy[1])

def MainFight(Left, Right):
    if max(Left[4], Right[4]) == Left[4]:
        #P1 = Player(LCurrentHP, LMaxHP, LAttack, LArmor, LSpeed, LItems, LLevel, LGold, "First")
        P1 = Player(Left, "First")
        #P2 = Player(RCurrentHP, RMaxHP, RAttack, RArmor, RSpeed, RItems, RLevel, RGold, "Second")
        P2 = Player(Right, "Second")
        Players = ["Left", "Right"]
    else:
        #P2 = Player(LCurrentHP, LMaxHP, LAttack, LArmor, LSpeed, LItems, LLevel, LGold, "Second")
        P2 = Player(Left, "Second")
        #P1 = Player(RCurrentHP, RMaxHP, RAttack, RArmor, RSpeed, RItems, RLevel, RGold, "First")
        P1 = Player(Right, "First")
        Players = ["Right", "Left"]


    #battlestart Phase
    P1.Search("BombBonus", P2)
    P2.Search("BombBonus", P1)
    P1.Search("BattleStart", P2)
    P2.Search("BattleStart", P1)


    #COULD just have a turn 1 line set so it doesnt check if its turn 1 every single turn
    #And then loop through the 2-40 turns
    for turn in range(0, 40):
            #Turn Xa
            TurnCount(P1, P2, turn) #Turn Start including first turn extra work

            #First Player's Strikes
            if (P1.Stun <= 0) and (P1.Count("CantAttack") == 0):
                for i in range(0, P1.StrikesCount):
                    P2 = P1.Strike(P2) #Strike
                    if checkLife(P1, P2, Players) == 1:
                        break

            #PostTurn Stuff for firstturn
            EndTurn(P1, P2, turn)

            if checkLife(P1, P2, Players) == 1:
                    break

            #Turn Xb
            TurnCount(P2, P1, turn) #Turn Start including first turn extra work

            #Second Player's Strikes
            if (P2.Stun <= 0) and (P2.Count("CantAttack") == 0):
                for i in range(0, P2.StrikesCount):
                    P1 = P2.Strike(P1) #Strike
                    if checkLife(P1, P2, Players) == 1:
                        break

            #PostTurn Stuff for firstturn
            EndTurn(P2, P1, turn)

            if checkLife(P1, P2, Players) == 1:
                    break
            


    if P1.CurrentHP <= 0:
        EndBattleHeal(P2, P1)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Player", Players[0], "has died first")
        print("Player", Players[1], "has won:", P2.CurrentHP,"/", P2.MaxHP, "HP", P2.Armor, "Armor", P2.Attack, "Attack")
        Result = f"Player {Players[0]} hase died first. Player {Players[1]} has won: {P2.CurrentHP} / {P2.MaxHP} HP {P2.Armor} Armor {P2.Attack} Attack"

    if P2.CurrentHP <= 0:
        EndBattleHeal(P1, P2)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Player", Players[1], "has died first")
        print("Player", Players[0], "has won:", P1.CurrentHP,"/", P1.MaxHP, "HP", P1.Armor, "Armor", P1.Attack, "Attack")
        Result = f"Player {Players[1]} hase died first. Player {Players[0]} has won: {P1.CurrentHP} / {P1.MaxHP} HP {P1.Armor} Armor {P1.Attack} Attack"

    return Result