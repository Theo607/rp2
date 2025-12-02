#ifndef BINS_HPP
#define BINS_HPP

#include <random>
#include <vector>
#include <cstddef>
#include <stdexcept>

struct bins {
private:
    std::size_t size = 0;
public:
    std::mt19937_64 rng;                 // single RNG
    std::uniform_int_distribution<std::size_t> dist;
    std::vector<std::size_t> arr;
    std::size_t empty_bins;              // track number of empty bins
    bool first_collision = false;

    explicit bins(std::size_t s, unsigned long seed = std::random_device{}())
        : size(s), arr(s, 0), empty_bins(s), rng(seed), dist(0, s - 1)
    {
        if (size == 0) {
            throw std::invalid_argument("bins size must be > 0");
        }
    }

    // Reset all bins
    void clear() {
        arr.assign(size, 0);
        empty_bins = size;
        first_collision = false;
    }

    // Add multiple balls
    void add_balls(std::size_t balls) {
        for (std::size_t i = 0; i < balls; ++i) {
            add_ball();
        }
    }

    // Add a single ball
    void add_ball() {
        std::size_t idx = dist(rng);
        if (arr[idx] == 0) empty_bins--;      // decrement empty bin counter
        if (++arr[idx] > 1) first_collision = true;
    }

    // Access a specific bin
    std::size_t bin_value(std::size_t index) const {
        if (index >= size)
            throw std::out_of_range("Index out of range in bins::bin_value");
        return arr[index];
    }

    // Number of empty bins
    std::size_t get_empty_bins() const {
        return empty_bins;
    }

    // Access all bins
    std::vector<std::size_t>& get_bins() {
        return arr;
    }
};

#endif // BINS_HPP
