# Modelling the ecosystem of Rossumøya
This project is a development of a population dynamic
simulation. 
The development team consists of two NMBU students; Nina Mariann Vesseltun
 and Trude Haug Almestrand. The simulation consists of a series of biomes
and two species of animals (one carnivore and one herbivore) and simulates
 their migration, reproduction and eating over the course of some turns (years)
  
 ## How biomes work
 The biomes are tilebased with ocean covering the top and bottom, and sides
  of the map so that it simulates an island. There are two impassable biome
   tiles: ocean and mountain. Meaning that herbivores and carnivores can not
    enter these tiles. They are restricted to only entering savannahs
    , deserts and jungle. Savannahs has limited fodder whereas jungle is
     fast growing and has "unlimited" fodder. Savannahs replenish their
      fodder slowly (over several years depending on the number of
       individual herbivores) whilst
       jungle replenishes theirs to max after one year.
    
 ## The animals
 Herbivores graze on savannahs and jungle at a given value F. If there are
  multiple individuals grazing, the resources can deplete and thus no food
   be available to the herbivore. The order of who gets to eat is determined
    by an animals fitness. Weight is gained based off of how much they eat and fitness is based off
   of a gaussian distribution.
   
   Carnivores are dependent on herbivores for food and are therefore more
    mobile than herbivores. They can only eat herbivores and only if they
     are on the same tile as them. If there are multiple herbivores then
      they eat the ones with the lowest fitness. Weight gained is equivalent
       to the weight from the eaten herbivore. Carnivores can only eat
        herbivores with a lower fitness than themselves (DARWIN)
        
 ## Movement
 Movement is based off of fodder available and the amount of individuals of
 the same species present. Together with a probability of moving. Carnivores
  are more mobile and have a higher percentage chance of moving. 