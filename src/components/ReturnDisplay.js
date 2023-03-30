function ReturnDisplay({ returns }) {
    return (
        returns['1'] !== undefined ? 
        <div>
            <p className={returns['30'] >= 0 ? 'investment-return-positive' : 'investment-return-negative'}>30d: {returns['30']+'%'}</p>
            <p className={returns['5'] >= 0 ? 'investment-return-positive' : 'investment-return-negative'}>5d: {returns['5']+'%'}</p>
            <p className={returns['1'] >= 0 ? 'investment-return-positive' : 'investment-return-negative'}>1d: {returns['1']+'%'}</p>
        </div>
        : null
    );
}

export default ReturnDisplay;