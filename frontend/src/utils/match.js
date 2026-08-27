export const getMatchResult = (match) => {
    if (!match || match.status !== 'completed') {
        return null
    }

    if (match.our_score > match.opponent_score) {
        return 'win'
    }

    if (match.our_score < match.opponent_score) {
        return 'loss'
    }

    return 'draw'
}

export const matchResultLabels = {
    win: 'Win',
    draw: 'Draw',
    loss: 'Loss',
}