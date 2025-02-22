import HomeImg from "../components/HomeImg";
import SignupButton from "../components/SignupButton";
import Features from "../components/Features";
import Letters from "../components/Letters";

function HomePage() {
    return (
        <>
        <HomeImg />
        <SignupButton text="🚀 Sign In" link="/signup" />
        <Features />
        <Letters />
        </>
    );
}

export default HomePage;