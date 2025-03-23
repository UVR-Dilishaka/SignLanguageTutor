export const fetchSigns = async (userId, language, navigate) => {
    try {
      const response = await fetch(`http://localhost:5000/tutorSystem/getnextsigns/${userId}/${language}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error(`Error fetching signs: ${response.statusText}`);
      }
  
      const signsData = await response.json();
      return signsData;
    } catch (error) {
      console.error('Error fetching signs:', error);
      navigate('/error');  // Redirect to an error page if something goes wrong
      return null;
    }
  };
  