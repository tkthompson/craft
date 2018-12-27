import game_objects as game

#test stuff below

#test_object = game.Item("Test Object", 100, {"temperature":50, "mass":1000, "length":10, "width":10, "height":10, "gas":300, "liquid":200, "solid":100})
#test_object = game.Item(file = "obj/test_object.json")

#test_object.jsonify("test_object.json")

"""
#Test Logging
game_log = game.GameLogger("testlog.log")
game_log.msg("jsonify(test_object) returned " + str(test_object.jsonify("test_object.json")))
game_log.msg("Testing flair creation", flair = game_log.Flair(function = "new", flair = ["Terst"]))
game_log.msg("Testing flair recreation", flair = game_log.Flair(function = "new", flair = ["Test"]))
game_log.msg("Testing flair adding", flair = game_log.Flair(function = "add", flair = ["Test1","Test2"]))
game_log.msg("Testing flair deletion", flair = game_log.Flair(function = "del", flair = ["Test1"]))
game_log.msg("Testing flair without arguments", flair = game_log.Flair())
game_log.msg("Testing flair resetting", flair = game_log.Flair(function = "new"))
game_log.msg("Testing flair empty arguments", flair = game_log.Flair(flair = ["Test1","","Test3","","Test5"]))
"""