export const service_wallet = 'cactus_wallet';
export const service_full_node = 'cactus_full_node';
export const service_farmer = 'cactus_farmer';
export const service_harvester = 'cactus_harvester';
export const service_simulator = 'cactus_full_node_simulator';
export const service_daemon = 'daemon';
export const service_plotter = 'cactus plots create';

// Corresponds with outbound_message.py NodeTypes
export const service_connection_types = {
  1: 'Full Node',
  2: 'Harvester',
  3: 'Farmer',
  4: 'Timelord',
  5: 'Introducer',
  6: 'Wallet',
  7: 'Plotter',
};
