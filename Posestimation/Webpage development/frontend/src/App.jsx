import Canvas from './Canvas.jsx';
import FullScreenButton from './FullScreenButton.jsx';
import Header from './Header.jsx'
import Hint from './Hint.jsx';
import LetterSwitch from './LetterSwitch.jsx';
import LevelLetters from './LevelLetters.jsx';
import LevelNo from './LevelNo.jsx';
import Score from './score.jsx';

function App() {
    return (<>
        <Header/>
        <div className='main-level-container'>
            <LevelNo/>
            <LevelLetters/>
            <Score/>
        </div>
        <div className='sign-related-container'>
            <Canvas/>
            <Hint/>
            <LetterSwitch/>
        </div>
        <FullScreenButton/>
    </>);
}

export default App
