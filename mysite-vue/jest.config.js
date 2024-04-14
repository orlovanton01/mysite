module.exports = {
    // moduleNameMapper: {
    //     "^@/(.*)$": "<rootDir>/src/$1"
    // },
    // transform: {
    //     "^.+\\.vue$": "@vue/vue3-jest"
    // }
    moduleFileExtensions: ['js', 'jsx', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.(js|jsx)?$': 'babel-jest'
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  snapshotSerializers: ['jest-serializer-vue'],
//   testMatch: [
//     '<rootDir>/(tests/unit/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx))'
//   ],
  transformIgnorePatterns: ['<rootDir>/node_modules/', "node_modules/(?!@ngrx|(?!deck.gl)|ng-dynamic)"]
}