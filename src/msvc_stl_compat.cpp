#include <cstddef>

// Stub for __std_find_last_not_ch_pos_1, a vectorized MSVC STL intrinsic
// that ICU references but that is not resolved when linking across CRT versions.
// This non-vectorized fallback is functionally correct.
extern "C" size_t __std_find_last_not_ch_pos_1(
    const void* const haystack,
    const size_t length,
    const unsigned char needle) noexcept
{
    const unsigned char* const data = static_cast<const unsigned char*>(haystack);
    for (size_t i = length; i != 0; --i) {
        if (data[i - 1] != needle) {
            return i - 1;
        }
    }
    return static_cast<size_t>(-1);
}
