const Features = () => {
    const featureList = [
      { text: "AI-Powered Sign Recognition" },
      { text: "Real-Time Feedback" },
      { text: "Interactive Learning" },
      { text: "Games & Videos" },
      { text: "Progress Tracking" },
    ];
  
    return (
      <div>
        <h2>🎯 Activities in Our System</h2>
        <div className="features">
          {featureList.map((feature, index) => (
            <div key={index} className="feature">
              {feature.text}
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  export default Features;
  