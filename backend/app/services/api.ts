
const generateUXKit = async (input: BrandInput): Promise<UXKit> => {
  const res = await fetch('/api/v1/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });
  return res.json();
};