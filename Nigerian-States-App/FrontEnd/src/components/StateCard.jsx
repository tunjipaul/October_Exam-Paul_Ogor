

function StateCard({ state }) {
    return (
        <div className="card">
            <h2 className="card-title">{state.name}</h2>
            <p className="text">Capital: {state.capital}</p>
            <p className="text">Region: {state.region}</p>
            <p className="text">Population: {state.population}</p>
            <p className="text">Slogan: {state.slogan}</p>
            <p className="text">Landmarks: {state.landmarks}</p>
        </div>
    );
}

export default StateCard;
