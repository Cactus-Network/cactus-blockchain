const cactus = require('../../util/cactus');

describe('cactus', () => {
  it('converts number mojo to cactus', () => {
    const result = cactus.mojo_to_cactus(1000000);

    expect(result).toBe(0.000001);
  });
  it('converts string mojo to cactus', () => {
    const result = cactus.mojo_to_cactus('1000000');

    expect(result).toBe(0.000001);
  });
  it('converts number mojo to cactus string', () => {
    const result = cactus.mojo_to_cactus_string(1000000);

    expect(result).toBe('0.000001');
  });
  it('converts string mojo to cactus string', () => {
    const result = cactus.mojo_to_cactus_string('1000000');

    expect(result).toBe('0.000001');
  });
  it('converts number cactus to mojo', () => {
    const result = cactus.cactus_to_mojo(0.000001);

    expect(result).toBe(1000000);
  });
  it('converts string cactus to mojo', () => {
    const result = cactus.cactus_to_mojo('0.000001');

    expect(result).toBe(1000000);
  });
  it('converts number mojo to colouredcoin', () => {
    const result = cactus.mojo_to_colouredcoin(1000000);

    expect(result).toBe(1000);
  });
  it('converts string mojo to colouredcoin', () => {
    const result = cactus.mojo_to_colouredcoin('1000000');

    expect(result).toBe(1000);
  });
  it('converts number mojo to colouredcoin string', () => {
    const result = cactus.mojo_to_colouredcoin_string(1000000);

    expect(result).toBe('1,000');
  });
  it('converts string mojo to colouredcoin string', () => {
    const result = cactus.mojo_to_colouredcoin_string('1000000');

    expect(result).toBe('1,000');
  });
  it('converts number colouredcoin to mojo', () => {
    const result = cactus.colouredcoin_to_mojo(1000);

    expect(result).toBe(1000000);
  });
  it('converts string colouredcoin to mojo', () => {
    const result = cactus.colouredcoin_to_mojo('1000');

    expect(result).toBe(1000000);
  });
});
