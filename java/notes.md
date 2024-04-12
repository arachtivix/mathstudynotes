this is just a placeholder

I want to look into how 

hashmap.computeIfAbsent(...,() -> new ArrayList())

compares to 

v = hashmap.getOrDefault(...,new ArrayList())
hashmap.put(...,v)

in terms of execution time.  Intuitively to me the latter is less efficient because it instantiates the list every time regardless of whether the ... key was in the map, so if there are many reuses of a given key, it should be less wasteful, but I want to be more rigorous 