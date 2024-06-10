import map

class Room():
    def __init__(self) -> None:
        self.my_maps = []
        self.is_first_time = {}
        self.import_maps(9, self.my_maps)
        self.first_time_in_room(9, self.is_first_time)
        self.current_map_position = 0
        self.current_room().map_npc_define()

    def import_maps(self, number_of_maps: int, maps_vector= []) -> None:
        """Acessa a pasta Tiled e guarda os mapas (arquivos tmx) em um vetor de mapas

        Args:
            number_of_maps: número de mapas desejados
            maps_vector: vetor que vai armazenar os mapas
        """
        for i in range(number_of_maps):
            current_map = map.Map(f"Tiled/Map{i}.tmx")
            maps_vector.append(current_map) 

    def first_time_in_room(self, number_of_maps: int, first_time_dictionary= {}) -> None:
        """Inicializa o dictionary de primeira vez na sala com True
        
        Args:
            number_of_maps: número de mapas existentes
            first_time_dictionary: dictionary que vai armazenar se é a primeira vez na sala
        """
        for i in range(number_of_maps):
            first_time_dictionary[i] = True

    def current_room(self) -> map:
        return self.my_maps[self.current_map_position]
    
    def advance_room(self) -> None:
        """Aumenta o índice do vetor de mapas
        
        """
        self.current_map_position += 1
        self.current_room().map_number = self.current_map_position

    def return_room(self) -> None:
        """Diminui o índice do vetor de mapas
        
        """
        self.current_map_position -= 1
        self.current_room().map_number = self.current_map_position

    def current_room_npc(self):
        if self.current_map_position == 0:
            return self.current_room().npc
        else:
            return None

