const apiUrl = 'http://192.168.1.2:8000/login';

const fetchData = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/endpoint`);
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

fetchData()