import React, { forwardRef } from "react";

const Timer = forwardRef((props, ref) => {
    return <div className="timer" ref={ref}>You have: {props.time}</div>;
});

export default Timer;
