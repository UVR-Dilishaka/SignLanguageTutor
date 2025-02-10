import { useState } from "react"
import { useEffect } from "react"


function App() {
    const [message, setMessage] = useState("Loading...");

    useEffect(() => {
        fetch("/data/ping-public")
            .then(response => response.json())
            .then(data => {
                if (data.txt) {
                    setMessage(data.txt);
                } else {
                    setMessage("No message found");
                }
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                setMessage("Failed to load data");
            });
    }, []);

    return (
        <div className="test">
            {message}
        </div>
    );
}

export default App
