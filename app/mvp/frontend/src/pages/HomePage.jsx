import HomeImg from "../components/HomeImg";
import SignupButton from "../components/SignupButton";
import Features from "../components/Features";
import Letters from "../components/Letters";
import Header from "../components/Header";

function HomePage() {
    return (
        <>
        <Header />
        <HomeImg />
        <SignupButton text="🚀 Sign In" link="/signup" />
        <Letters />
        <Features />
        
        </>
    );
}

export default HomePage;