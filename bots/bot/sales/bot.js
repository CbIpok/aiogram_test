const mineflayer = require('mineflayer')
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder')
const pvp = require('mineflayer-pvp').plugin
const { mineflayer: mineflayerViewer } = require("prismarine-viewer");
const maps = require('mineflayer-maps')
const autoeat = require('mineflayer-auto-eat').plugin
const { Telegraf } = require('telegraf')

const telegram = new Telegraf("6266423209:AAELJVUN0eDzto-tgnZRe3gRY9KHBVMNJlE")

const options = {
  //host: '192.168.31.153',
  host: '51.38.130.29',
  port: 25565,
  username: 'Tommy',
  //maps_outputDir: "output/"
}

const bot = mineflayer.createBot(options)
//bot.loadPlugin(maps)
bot.loadPlugin(pathfinder)
bot.loadPlugin(pvp)
bot.loadPlugin(autoeat)

let isReady = false;

bot.once('spawn', () => {
	isReady = false;
	const chestBlocks = bot.findBlocks({ matching: [54], maxDistance: 128, count: 10 });
	if (chestBlocks.length > 0) {
		console.log(`Found ${chestBlocks.length} chests:`);
		chestBlocks.forEach((block) => {
			console.log(block);
		});
	} else {
		console.log('No chests found');
    }
  
    bot.autoEat.options = {
		priority: 'foodPoints',
		startAt: 16,
		bannedFood: ['golden_apple', 'enchanted_golden_apple', 'pufferfish', 'spider_eye', 'poisonous_potato', 'rotten_flesh']
    }
    mineflayerViewer(bot, { port: 3007, firstPerson: true });

});

bot.once('resourcePack', () => { // resource pack sent by server
  bot.acceptResourcePack()
})

let guardPos = null

// Assign the given location to be guarded
function guardArea (pos) {
  guardPos = pos

  // We we are not currently in combat, move to the guard pos
  if (!bot.pvp.target) {
    moveToGuardPos()
  }
}

// Cancel all pathfinder and combat
function stopGuarding () {
  guardPos = null
  bot.pvp.stop()
  bot.pathfinder.setGoal(null)
}

// Pathfinder to the guard position
function moveToGuardPos () {
  bot.pathfinder.setMovements(new Movements(bot))
  bot.pathfinder.setGoal(new goals.GoalBlock(guardPos.x, guardPos.y, guardPos.z))
}

// Called when the bot has killed it's target.
bot.on('stoppedAttacking', () => {
    if (guardPos) moveToGuardPos()
})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
bot.on('death', () => {
	bot.chat("/tp ~ ~ ~")
	console.log("Successful attempt")
})

bot.on('spawn', () => {
	if (isReady) {
		console.log("Spawned")
		bot.chat("rtp")
		setTimeout( () => { console.log('Hello after 10 seconds'); }, 10 * 1000 );
	}
	console.log("spawned")
})

// Check for new enemies to attack
bot.on('physicsTick', () => {
  if (!guardPos) return // Do nothing if bot is not guarding anything

  // Only look for mobs within 16 blocks
  const filter = e => e.type === 'mob' && e.position.distanceTo(bot.entity.position) < 16 &&
                    e.mobType !== 'Armor Stand' // Mojang classifies armor stands as mobs for some reason?

  const entity = bot.nearestEntity(filter)
  if (entity) {
    // Start attacking
    bot.pvp.attack(entity)
  }
})


telegram.on('text', async (ctx) => {
    if (ctx.update.message.chat.id.toString() === "251181661") {
	    message = ctx.message.text
	    if (message === 'stop') { stopGuarding() }
	    if (message === 'equip') { equipItem('diamond_sword', 'hand') }
		if (message === 'items') { sayItems() }
		if (message === 'map') { equipItem('filled_map', 'hand') }
		if (message.split(" ")[0] === "say") { 
			w = message.split(" ")
			w.shift()
			bot.chat(w.join(" ")) 
		}
		if (message === 'turn on') { 
			isReady = true; 
		}
    }
})


bot.on('chat', (username, message) => {
    if (username != bot.username) telegram.telegram.sendMessage("251181661", username + ': ' + message)
    if (username != "Tommywh" && username != "Tommy") return
    // Guard the location the player is standing
    if (message === 'guard') {
        const player = bot.players[username]

        if (!player) {
            console.log("I can't see you.")
            return
        }

        console.log('I will guard that location.')
        guardArea(player.entity.position)
    }

  // Stop guarding
  if (message === 'stop') {
    console.log('I will no longer guard this area.')
    stopGuarding()
  }
  
  if (message === 'equip') { equipItem('diamond_sword', 'hand') }
  if (message === 'items') { sayItems() }
  if (message === 'map') { equipItem('filled_map', 'hand') }
});


async function equipItem (name, destination) {
  const item = itemByName(name)
  if (item) {
    try {
      await bot.equip(item, destination)
      console.log(`equipped ${name}`)
    } catch (err) {
      console.log(`cannot equip ${name}: ${err.message}`)
    }
  } else {
    console.log(`I have no ${name}`)
  }
}


function sayItems (items = null) {
  if (!items) {
    items = bot.inventory.items()
    if (bot.registry.isNewerOrEqualTo('1.9') && bot.inventory.slots[45]) items.push(bot.inventory.slots[45])
  }
  const output = items.map(itemToString).join(', ')
  if (output) {
    console.log(output)
  } else {
    console.log('empty')
  }
}


function itemToString (item) {
	if (item) { return `${item.name} x ${item.count}` }
	return '(nothing)'
}


function itemByName (name) {
	const items = bot.inventory.items()
	if (bot.registry.isNewerOrEqualTo('1.9') && bot.inventory.slots[45]) items.push(bot.inventory.slots[45])
	return items.filter(item => item.name === name)[0]
}

bot.on('autoeat_started', () => {
	console.log('Auto Eat started!')
})

bot.on('autoeat_stopped', () => {
	console.log('Auto Eat stopped!')
})
/**
bot.on('health', () => {
  if (bot.food === 20) bot.autoEat.disable()
  // Disable the plugin if the bot is at 20 food points
  else bot.autoEat.enable() // Else enable the plugin again
})
**/
telegram.launch()